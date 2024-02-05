import React, { useState } from "react";
import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  IconButton,
  TextField,
  Typography,
} from "@mui/material";
import CheckIcon from "@mui/icons-material/Check";
import CloseIcon from "@mui/icons-material/Close";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import copy from "copy-to-clipboard";

function DeleteDataProfileWindow({
  open,
  onClose,
  dataProfileToDelete,
  onDelete,
}) {
  const [isCopied, setIsCopied] = useState(false);
  const [isFilled, setIsFilled] = useState(false);
  const [confirmDataProfile, setConfirmDataProfile] = useState("");

  const handleDelete = () => {
    if (confirmDataProfile === dataProfileToDelete) {
      setConfirmDataProfile("");
      setIsFilled(false);
      onDelete();
    } else {
      alert("The entered name does not match the data profile to be deleted.");
    }
  };

  const handleCopy = () => {
    copy(dataProfileToDelete);
    setIsCopied(true);
    setTimeout(() => {
      setIsCopied(false);
    }, 2000); // change back to original icon after 2 seconds
  };

  const handleClose = () => {
    setConfirmDataProfile("");
    setIsFilled(false);
    onClose();
  };

  return (
    <Dialog
      open={open}
      onClose={handleClose}
      sx={{ "& .MuiDialog-paper": { width: "400px" } }}
    >
      <IconButton
        onClick={handleClose}
        sx={{ position: "absolute", right: 8, top: 8 }}
      >
        <CloseIcon />
      </IconButton>
      <DialogTitle>Delete Data Profile</DialogTitle>
      <DialogContent>
        <DialogContentText>
          Deleting a data profile is permanent and cannot be undone.
          <br /> <br />
          Enter the data profile name below to confirm.
        </DialogContentText>

        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            border: "1px solid darkgrey",
            borderRadius: "4px",
            my: 2,
            backgroundColor: "#f0f0f0",
          }}
        >
          <Box sx={{ py: 2, pl: 2 }}>{dataProfileToDelete}</Box>
          <IconButton
            onClick={handleCopy}
            sx={{
              py: 2,
              pl: 2,
              pr: 2,
              backgroundColor: "white",
              borderRadius: "0",
              height: "100%",
              borderLeft: "1px solid darkgrey",
            }}
          >
            {isCopied ? <CheckIcon /> : <ContentCopyIcon />}
          </IconButton>
        </Box>

        <Typography variant="body1" sx={{ fontWeight: "bold", mb: 1 }}>
          Data profile name <span style={{ color: "red" }}>*</span>
        </Typography>

        <TextField
          autoFocus
          margin="dense"
          label={!isFilled ? "Enter the name of the data profile" : null}
          type="text"
          fullWidth
          value={confirmDataProfile}
          onChange={(e) => {
            setConfirmDataProfile(e.target.value);
            setIsFilled(e.target.value !== "");
          }}
          InputLabelProps={{ shrink: false }}
        />
      </DialogContent>
      <DialogActions sx={{ pb: 2, pr: 2 }}>
        <Button onClick={onClose}>Cancel</Button>
        <Button
          onClick={handleDelete}
          autoFocus
          disabled={confirmDataProfile !== dataProfileToDelete}
          sx={{
            color: "white",
            backgroundColor:
              confirmDataProfile === dataProfileToDelete
                ? "#b71c1c"
                : "#b71c1c80",
            "&:hover": {
              backgroundColor:
                confirmDataProfile === dataProfileToDelete
                  ? "#7f0000"
                  : "#7f000080",
            },
            "&.Mui-disabled": {
              color: "white", // keep the text color white when the button is disabled
            },
          }}
        >
          Delete
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default DeleteDataProfileWindow;
