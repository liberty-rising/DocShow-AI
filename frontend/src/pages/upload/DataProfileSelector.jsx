import React, { useState } from "react";
import {
  FormControl,
  IconButton,
  InputLabel,
  ListItemText,
  MenuItem,
  Select,
} from "@mui/material";
import Delete from "@mui/icons-material/Delete";

const DataProfileSelector = ({
  dataProfiles,
  dataProfile,
  setDataProfile,
  handleOpenDeleteDialog,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const isValidDataProfile = dataProfiles.includes(dataProfile);
  const safeDataProfile = isValidDataProfile ? dataProfile : "";

  const handleOpen = () => {
    setIsOpen(true);
  };

  const handleClose = () => {
    setIsOpen(false);
  };

  return (
    <FormControl fullWidth>
      <InputLabel id="data-profile-label">Choose a data profile</InputLabel>
      <Select
        labelId="data-profile-label"
        value={safeDataProfile}
        label="Choose a data profile"
        onChange={(e) => setDataProfile(e.target.value)}
        onOpen={handleOpen}
        onClose={handleClose}
        renderValue={(selected) => <ListItemText primary={selected} />}
      >
        {dataProfiles.map((profile, index) => (
          <MenuItem key={index} value={profile}>
            <ListItemText primary={profile} />
            {isOpen && (
              <IconButton
                edge="end"
                aria-label="delete"
                onClick={() => handleOpenDeleteDialog(profile)}
              >
                <Delete />
              </IconButton>
            )}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default DataProfileSelector;
