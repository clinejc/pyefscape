#pragma once

/**
Defines the arrowice interface, an interface for an Apache Arrow IPC-based
framework.
*/
module arrowice {


    sequence<byte> ByteList;
    sequence<string> StringList;

    /**
     * ArrowTable -- a structure for holding Arrow tables
     */
    struct ArrowTable {
        ByteList data;  // Serialized Arrow table in IPC format
    };

    interface ArrowServer {
        ArrowTable getTable(string tableName);
        void uploadTable(string tableName, ArrowTable table);
        string getTableSchema(string tableName);
        StringList listTableNames();
    };
};
