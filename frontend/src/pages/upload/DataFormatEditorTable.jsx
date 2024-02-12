import React, { useEffect, useState } from "react";
import { Column } from "primereact/column";
import { Dropdown } from "primereact/dropdown";
import { DataTable } from "primereact/datatable";
import { InputText } from "primereact/inputtext";
import { RadioButton } from "primereact/radiobutton";

function DataFormatEditorTable({
  previewData,
  setPreviewData,
  availableColumnTypes,
  columnMetadata,
  setColumnMetadata,
  primaryKey,
  setPrimaryKey,
}) {
  const EditableInputText = ({
    columnName,
    previewData,
    setPreviewData,
    columnMetadata,
    setColumnMetadata,
  }) => {
    const [editedColumnName, setEditedColumnName] = useState(
      columnName.replace(/_/g, " ").toUpperCase(),
    );

    return (
      <InputText
        style={{ width: "100%", height: "100%" }}
        value={editedColumnName}
        onChange={(e) => {
          setEditedColumnName(e.target.value);
        }}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            e.target.blur();
          }
        }}
        onFocus={(e) => {
          e.target.select();
        }}
        onBlur={(e) => {
          const newColumnName = e.target.value.replace(/ /g, "_").toLowerCase();

          if (newColumnName !== columnName) {
            const newPreviewData = previewData.map((row) => {
              const newRow = Object.keys(row).reduce((acc, key) => {
                if (key === columnName) {
                  acc[newColumnName] = row[key];
                } else {
                  acc[key] = row[key];
                }
                return acc;
              }, {});

              return newRow;
            });

            // Update the previewData state
            setPreviewData(newPreviewData);

            // Update the columnMetadata state if column name is changed
            const newColumnMetadata = { ...columnMetadata };
            newColumnMetadata[newColumnName] = newColumnMetadata[columnName];
            if (
              newColumnMetadata[columnName] &&
              newColumnMetadata[columnName].primary_key
            ) {
              newColumnMetadata[newColumnName].primary_key = true;
              delete newColumnMetadata[columnName];
            }
            setColumnMetadata(newColumnMetadata);

            // Reset the editedColumnName state
            setEditedColumnName(newColumnName.replace(/_/g, " ").toUpperCase());
          }
        }}
      />
    );
  };
  return (
    <DataTable
      value={Object.keys(previewData[0]).map((columnName) => ({
        column: (
          <EditableInputText
            columnName={columnName}
            previewData={previewData}
            setPreviewData={setPreviewData}
            columnMetadata={columnMetadata}
            setColumnMetadata={setColumnMetadata}
            primaryKey={primaryKey}
            setPrimaryKey={setPrimaryKey}
          />
        ),
        primaryKey: (
          <RadioButton
            name="primaryKey"
            checked={columnMetadata[columnName].primary_key}
            onChange={(e) => {
              // Create a copy of the columnMetadata state
              const newColumnMetadata = { ...columnMetadata };

              // Iterate over the newColumnMetadata object
              for (let key in newColumnMetadata) {
                // If the key matches the new primary key, set its primary_key attribute to true
                if (key === columnName) {
                  newColumnMetadata[key].primary_key = true;
                }
                // Otherwise, set the primary_key attribute to false
                else {
                  newColumnMetadata[key].primary_key = false;
                }
              }

              // Update the columnMetadata state
              setColumnMetadata(newColumnMetadata);
            }}
          />
        ),
        type: (
          <Dropdown
            value={columnMetadata[columnName]["data_type"]}
            options={availableColumnTypes.map((option) => ({
              label: option.charAt(0).toUpperCase() + option.slice(1),
              value: option,
            }))}
            filter
            onChange={(e) => {
              // Update the columnMetadata state here
              setColumnMetadata({
                ...columnMetadata,
                [columnName]: e.value,
              });
            }}
            style={{ width: "100%" }}
          />
        ),
      }))}
      paginator
      rows={5}
      rowsPerPageOptions={[5, 10, 25, 50]}
      paginatorTemplate="RowsPerPageDropdown FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
      currentPageReportTemplate="{first}-{last} of {totalRecords}"
      showGridlines
      resizableColumns
    >
      <Column field="column" header="COLUMN NAME" />
      <Column field="primaryKey" header="PRIMARY KEY" />
      <Column field="type" header="DATA TYPE" />
    </DataTable>
  );
}

export default DataFormatEditorTable;
