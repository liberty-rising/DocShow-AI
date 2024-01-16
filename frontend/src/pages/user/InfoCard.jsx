import React from "react";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";

const InfoCard = ({ Icon, title, content }) => (
  <Grid item xs={12} sm={6} md={4}>
    <Card>
      <CardContent>
        <Icon />
        <Typography variant="h6">{title}</Typography>
        <Typography variant="body1">{content}</Typography>
      </CardContent>
    </Card>
  </Grid>
);

export default InfoCard;
