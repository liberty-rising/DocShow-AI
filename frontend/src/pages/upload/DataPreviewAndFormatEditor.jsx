import React, { useState, useEffect } from "react";
import { Box, Tab, Tabs } from "@mui/material";
import DataFormatEditorTable from "./DataFormatEditorTable";
import DataPreviewTable from "./DataPreviewTable";
import TabPanel from "../../components/tabs/TabPanel";
import "primereact/resources/themes/lara-light-cyan/theme.css";
import "../../styles/tableStyles.css";

function DataPreviewAndFormatEditor({
  previewData,
  setPreviewData,
  availableColumnTypes,
  columnMetadata,
  setColumnMetadata,
}) {
  const [columns, setColumns] = useState([]);
  const [tabIndex, setTabIndex] = useState(0);

  useEffect(() => {
    if (Array.isArray(previewData) && previewData.length > 0) {
      const initialColumns = Object.keys(previewData[0]).map((key) => ({
        name: key,
      }));
      setColumns(initialColumns);
    }
  }, [previewData]);

  return (
    <Box>
      <Tabs
        value={tabIndex}
        onChange={(event, newValue) => setTabIndex(newValue)}
        centered
      >
        <Tab label="Data Preview" />
        <Tab label="Data Format Editor" />
      </Tabs>

      <TabPanel value={tabIndex} index={0}>
        <DataPreviewTable
          columnNames={columns.map((column) => column.name)}
          previewData={previewData}
        />
      </TabPanel>

      <TabPanel value={tabIndex} index={1}>
        <DataFormatEditorTable
          previewData={previewData}
          setPreviewData={setPreviewData}
          availableColumnTypes={availableColumnTypes}
          columnMetadata={columnMetadata}
          setColumnMetadata={setColumnMetadata}
        />
      </TabPanel>
    </Box>
  );
}

export default DataPreviewAndFormatEditor;
