import * as React from "react";
import {
  Container,
  Grid,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Box,
} from "@mui/material";

function PricingPage() {
  // Define the pricing tiers
  const tiers = [
    {
      title: "Starter",
      price: "190",
      description: ["1 User", "1 App", "Integrations"],
      buttonText: "Learn more",
      buttonVariant: "outlined",
    },
    {
      title: "Pro",
      price: "390",
      description: [
        "All in Starter plan",
        "Google Ads",
        "SSO via Google",
        "API access",
      ],
      buttonText: "Learn more",
      buttonVariant: "contained", // Change to contained for the middle button
    },
    {
      title: "Enterprise",
      price: "690",
      description: [
        "All features",
        "Email support",
        "Google Ads",
        "SSO via Google",
        "API access",
        "Facebook Ads",
      ],
      buttonText: "Learn more",
      buttonVariant: "outlined",
    },
  ];

  // Function to set the background color for the 'Pro' tier button
  const getButtonStyle = (title) => {
    return title === "Pro"
      ? { bgcolor: "primary.main", color: "common.white" }
      : {};
  };

  return (
    <Container maxWidth="md" component="main">
      <Box sx={{ my: { xs: 4, md: 8 } }}>
        <Typography
          component="h1"
          variant="h3"
          align="center"
          color="text.primary"
          gutterBottom
        >
          Flexible pricing options
        </Typography>
        <Typography
          variant="h6"
          align="center"
          color="text.secondary"
          component="p"
        >
          We are founded by a leading academic and researcher in the field of
          Industrial Systems Engineering. For entrepreneurs, startups and
          freelancers. If you didn’t find what you needed, these could help!
        </Typography>
        <Grid container spacing={5} alignItems="stretch">
          {tiers.map((tier) => (
            <Grid
              item
              key={tier.title}
              xs={12}
              sm={tier.title === "Enterprise" ? 12 : 6}
              md={4}
            >
              <Card
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  height: "100%",
                }}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography gutterBottom variant="h6" component="h2">
                    {tier.title}
                  </Typography>
                  <Typography variant="h4" color="text.primary">
                    ${tier.price}
                    <Typography
                      component="span"
                      variant="h6"
                      color="text.secondary"
                    >
                      /yr
                    </Typography>
                  </Typography>
                  <ul>
                    {tier.description.map((line) => (
                      <Typography
                        component="li"
                        variant="subtitle1"
                        align="center"
                        key={line}
                      >
                        {line}
                      </Typography>
                    ))}
                  </ul>
                </CardContent>
                <CardActions>
                  <Button
                    fullWidth
                    variant={tier.buttonVariant}
                    sx={{
                      ...getButtonStyle(tier.title),
                      justifyContent: "center",
                      mb: 2,
                      mt: "auto",
                    }}
                  >
                    {tier.buttonText}
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    </Container>
  );
}

export default PricingPage;
