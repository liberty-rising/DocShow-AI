import React from "react";
import { Link as RouterLink } from "react-router-dom";
import { Button } from "@mui/material";

const BlogLink = () => (
  <Button
    component={RouterLink}
    to="/blog"
    style={{ color: "#192b3e", marginRight: "20px" }}
  >
    Blog
  </Button>
);

export default BlogLink;
