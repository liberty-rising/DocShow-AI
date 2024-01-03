import { Typography, Grid } from '@mui/material';
import TableManagement from './TableManagement.jsx';
import UserManagement from './UserManagement.jsx';
import OrganizationManagement from './OrganizationManagement.jsx'; // Import the new component

function AdminPage() {
  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <Typography variant="h4">⚙️ Admin Panel</Typography>
      </Grid>
      <Grid item xs={12}>
        <TableManagement />
      </Grid>
      <Grid item xs={12}>
        <UserManagement />
      </Grid>
      <Grid item xs={12}>
        <OrganizationManagement /> {/* Add the new component here */}
      </Grid>
    </Grid>
  );
}

export default AdminPage;
