import axios from "axios";
import { API_URL } from "../utils/constants";

export const getPreviewData = (sampleFiles, extractInstructions) => {
  const formData = new FormData();
  sampleFiles.forEach((file) => {
    formData.append("files", file);
  });
  formData.append("extract_instructions", extractInstructions);

  return axios.post(`${API_URL}data-profiles/preview/`, formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};

export const getAvailableColumnTypes = () => {
  return axios.get(`${API_URL}data-profiles/column-types/`);
};

export const getSuggestedColumnMetadata = (previewData) => {
  return axios.post(`${API_URL}data-profiles/preview/column-metadata/`, {
    data: previewData,
  });
};
