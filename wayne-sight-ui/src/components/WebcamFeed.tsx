import { Box } from "@chakra-ui/react";

export const WebcamFeed = ({ videoRef }: any) => (
  <Box>
    <video
      ref={videoRef}
      autoPlay
      style={{ width: "100%", borderRadius: "8px" }}
    />
  </Box>
);
