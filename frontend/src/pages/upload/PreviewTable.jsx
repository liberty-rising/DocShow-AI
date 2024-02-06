import React, { useState, useEffect } from "react";

import { DataTable } from "primereact/datatable";
import { Column } from "primereact/column";
import { InputTextarea } from "primereact/inputtextarea";
import "primereact/resources/themes/lara-light-cyan/theme.css";
import "../../styles/tableStyles.css";
import { set } from "date-fns";

function PreviewTable({
  columnNames,
  previewData,
  onChangePreviewData,
  setIsEditingCell,
}) {
  const columns = columnNames.map((name) => ({
    Header: name.toUpperCase(),
    accessor: name,
  }));

  const data = previewData || [];

  const cellEditor = (options) => {
    setIsEditingCell(true);
    return textEditor(options);
  };

  const textEditor = (options) => {
    return (
      <InputTextarea
        autoResize={true}
        style={{ width: "100%", height: "100%" }}
        value={options.value}
        onChange={(e) => options.editorCallback(e.target.value)}
      />
    );
  };

  const onCellEditComplete = (e) => {
    let { rowData, newValue, field, originalEvent: event } = e;

    if (newValue.trim().length > 0) {
      onChangePreviewData(
        data.findIndex((row) => row === rowData),
        field,
        newValue,
      );
      setIsEditingCell(false);
    } else {
      event.preventDefault();
    }
  };

  return (
    <DataTable
      value={data}
      emptyMessage="Upload your files and click preview to see the data"
      paginator
      rows={5}
      rowsPerPageOptions={[5, 10, 25, 50]}
      paginatorTemplate="RowsPerPageDropdown FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
      currentPageReportTemplate="{first}-{last} of {totalRecords}"
      editMode="cell"
      resizableColumns
      scrollable
      scrollHeight="flex"
      showGridlines
      tableStyle={{ minWidth: "150px" }}
    >
      {columns.map((column) => (
        <Column
          key={column.accessor}
          field={column.accessor}
          header={column.Header}
          editor={(options) => cellEditor(options)}
          onCellEditComplete={onCellEditComplete}
          bodyClassName="multi-line"
        />
      ))}
    </DataTable>
  );
}

export default PreviewTable;
