import axios from "axios";
import { API_URL } from "./constants";

export const updateUserPassword = async (
  oldPassword,
  newPassword,
  confirmPassword,
  setErrorMessage,
  setSuccessMessage,
) => {
  if (newPassword !== confirmPassword) {
    setErrorMessage("Passwords do not match!");
    return false;
  }

  try {
    const response = await axios.put(`${API_URL}users/change-password/`, {
      old_password: oldPassword,
      new_password: newPassword,
    });

    console.log("Server response status:", response.status); // Add this line

    if (response.status === 200) {
      console.log("Password changed successfully");
      setSuccessMessage("Password changed successfully");
      setErrorMessage("");
      return true;
    } else {
      setErrorMessage("Failed to change password!");
      setSuccessMessage("");
      return false;
    }
  } catch (error) {
    if (error.response) {
      if (error.response.status === 400) {
        setErrorMessage(error.response.data.detail);
      } else if (
        error.response.data &&
        error.response.data.detail &&
        error.response.data.detail[0]
      ) {
        let errorMessage = error.response.data.detail[0].msg;
        if (typeof errorMessage === "string") {
          setErrorMessage(errorMessage);
        }
      }
    }
  }
  setErrorMessage(errorMessage);
  setSuccessMessage("");
  return false;
};
