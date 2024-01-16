import axios from "axios";
import { API_URL } from "../utils/constants";

export const fetchOrganizationTables = async (table) => {
  try {
    const user = await axios.get(`${API_URL}users/me/`);
    const response = await axios.get(
      `${API_URL}organization/${user.data.organization_id}/tables/`,
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching organization tables:", error);
    throw error;
  }
};
