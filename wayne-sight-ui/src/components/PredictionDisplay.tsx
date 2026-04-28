import { Card, Text, Box } from "@chakra-ui/react";

export const PredictionDisplay = ({ prediction }: { prediction: string }) => (
  <Card.Root variant="elevated" p={4} mt={4} maxW="md">
    <Card.Body>
      <Text textStyle="xl" fontWeight="bold" mb={2}>
        Prediction:
      </Text>
      <Text textStyle="2xl" color="blue.500" fontWeight="semibold">
        {prediction}
      </Text>
    </Card.Body>
  </Card.Root>
);
