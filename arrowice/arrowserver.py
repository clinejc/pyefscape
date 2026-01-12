import Ice
# import ArrowService
import pyarrow as pa
import pyarrow.ipc as ipc

import sys
from pathlib import Path
# import json
# import devs
import logging

# configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 1. set the path of the 'efscape' slice defitions
slice_dir = Path(__file__).parent.parent / "slice"

# 2. generate the python stubs for 'arrowice'
Ice.loadSlice(
    [
        "-I" + str(slice_dir),
        str(slice_dir / "arrowice" / "ArrowService.ice"),
    ]
)

# 3. import arrowice python API
import arrowice

# 4. define the ArrowServer class
class ArrowServerI(arrowice.ArrowServer):
    def __init__(self):
        self.tables = {}  # Store Arrow tables in memory
        # self._table = None

    # def setTable(self, table, current=None):
    #     self._table = table

    # def getTable(self, current=None):
    #     return self._table

    # def getTableSchema(self, current=None):
    #     return self._table.schema

    # def getTableData(self, current=None):
    #     return self._table.to_pandas()

    # def getTableDataAsJSON(self, current=None):
    #     return self._table.to_pandas().to_json()

    # def getTableDataAsArrow(self, current=None):
    #     return self._table

    # def getTableDataAsArrowStream(self, current=None):
    #     sink = pa.BufferOutputStream()
    #     writer = ipc.new_stream(sink, self._table.schema)
    #     writer.write_table(self._table)
    #     writer.close()
    #     return sink.getvalue()

    # def getTableDataAsArrowFile(self, file_path, current=None):
    #     with pa.OSFile(file_path, "wb") as sink:
    #         writer = ipc.new_file(sink, self._table.schema)
    #         writer.write_table(self._table)
    #         writer.close()

    # def getTableDataAsArrowFile(self, file_path, current=None):
    #     with pa.OSFile(file_path, "wb") as sink:
    #         writer = ipc.new_file(sink, self._table.schema)
    #         writer.write_table(self._table)
    #         writer.close()

    # def getTableDataAsArrowFile(self, file_path, current=None):
    #     with pa.OSFile(file_path, "wb") as sink:
    #         writer = ipc.new_file(sink, self._table.schema)
    #         writer.write_table(self._table)
    #         writer.close()

    # def getTableDataAsArrowFile(self, file_path, current=None):
    #     with pa.OSFile(file_path, "wb") as sink:
    #         writer = ipc.new_file(sink, self._table.schema)
    #         writer.write_table(self._table)
    #         writer.close()

    # def getTableDataAsArrowFile(self, file_path, current=None):
    #     with pa.OSFile(file_path, "wb") as sink:
    #         writer = ipc.new_file(sink, self._table.schema)
    #         writer.write_table(self._table)
    #         writer.close()

    # def getTableDataAsArrowFile(self, file_path, current=None):
    #     with pa.OSFile(file_path, "wb") as sink:
    #         writer = ipc

    def getTable(self, tableName, current=None):
        if tableName not in self.tables:
            raise RuntimeError(f"Table {tableName} not found")
        
        # Serialize the Arrow table to IPC format
        sink = pa.BufferOutputStream()
        writer = ipc.new_file(sink, self.tables[tableName].schema)
        writer.write_table(self.tables[tableName])
        writer.close()
        
        return arrowice.ArrowTable(data=sink.getvalue().to_pybytes())

    def uploadTable(self, tableName, table, current=None):
        # Convert the list of bytes (list[int]) back to a bytes object
        buffer = bytes(table.data)

        # Deserialize the Arrow table from the bytes
        source = pa.BufferReader(buffer)
        reader = ipc.open_file(source)
        self.tables[tableName] = reader.read_all()
        print(f"Uploaded table {tableName} with schema: {self.tables[tableName].schema}")

    def getTableSchema(self, tableName, current=None):
        """Return the schema of the specified table as a string."""
        if tableName not in self.tables:
            raise RuntimeError(f"Table {tableName} not found")
        return str(self.tables[tableName].schema)

    def listTableNames(self, current=None):
        """Return a list of all stored table names."""
        return list(self.tables.keys())


def main():
    with Ice.initialize(sys.argv) as communicator:
        adapter = communicator.createObjectAdapterWithEndpoints(
            "ArrowAdapter",
            "default -p 10000",
        )
        servant = ArrowServerI()
        adapter.add(servant, Ice.stringToIdentity("ArrowServer"))
        adapter.activate()
        print("ArrowServer is running...")
        communicator.waitForShutdown()


if __name__ == "__main__":
    main()
