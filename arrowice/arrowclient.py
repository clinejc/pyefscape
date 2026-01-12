import sys
import Ice
import pyarrow as pa
import pyarrow.ipc as ipc
from pathlib import Path

# 1. set the path of the 'efscape' slice defitions
slice_dir = Path(__file__).parent.parent / "slice"
print(f"slice_dir={slice_dir}")

# 2. generate the python stubs for 'arrowice'
Ice.loadSlice(
    [
        "-I" + str(slice_dir),
        str(slice_dir / "arrowice/ArrowService.ice"),
    ]
)

# 3. import arrowice python API
# import arrowice
from arrowice import (
    ArrowServerPrx,
    ArrowTable
)

def serialize_table(table):
    """Serialize an Arrow table to IPC format and return as bytes."""
    sink = pa.BufferOutputStream()
    writer = ipc.new_file(sink, table.schema)
    writer.write_table(table)
    writer.close()
    return sink.getvalue().to_pybytes()

def deserialize_table(data):
    """Deserialize an Arrow table from IPC format."""
    # Convert list[int] to bytes
    buffer = bytes(data)
    source = pa.BufferReader(buffer)
    reader = ipc.open_file(source)
    return reader.read_all()

def main():
    with Ice.initialize(sys.argv) as communicator:
        # Connect to the server
        proxy = communicator.stringToProxy("ArrowServer:default -p 10000")
        server = ArrowServerPrx.checkedCast(proxy)
        if not server:
            raise RuntimeError("Invalid proxy")

        # Create and upload a table
        table = pa.table({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
        serialized_data = serialize_table(table)
        arrow_table = ArrowTable(data=list(serialized_data))
        server.uploadTable("example_table", arrow_table)

        # Retrieve the table schema
        schema = server.getTableSchema("example_table")
        print("Schema for 'example_table':")
        print(schema)

        # List all table names
        table_names = server.listTableNames()
        print("List of all table names:")
        print(table_names)

        # Retrieve the table
        retrieved = server.getTable("example_table")
        deserialized_table = deserialize_table(retrieved.data)  # Convert list back to bytes
        print("Retrieved table:")
        print(deserialized_table)

if __name__ == "__main__":
    main()
