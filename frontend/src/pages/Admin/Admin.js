import { Typography, Grid } from '@mui/material';
import TableManagement from './TableManagement';
import UserManagement from './UserManagement';

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
    </Grid>
  );
}

export default AdminPage;