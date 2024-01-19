import React from "react";
import { FormControl, InputLabel, MenuItem, Select } from "@mui/material";

const DataProfileSelector = ({ dataProfiles, dataProfile, setDataProfile }) => {
  const isValidDataProfile = dataProfiles.includes(dataProfile);
  const safeDataProfile = isValidDataProfile ? dataProfile : "";

  return (
    <FormControl fullWidth>
      <InputLabel id="data-profile-label">Choose a data profile</InputLabel>
      <Select
        labelId="data-profile-label"
        value={safeDataProfile}
        label="Choose a data profile"
        onChange={(e) => setDataProfile(e.target.value)}
      >
        {dataProfiles.map((profile, index) => (
          <MenuItem key={index} value={profile}>
            {profile}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default DataProfileSelector;
