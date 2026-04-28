import { Flex } from "@chakra-ui/react";
import { MainLayout } from "./components/MainLayout";
import { PredictionDisplay } from "./components/PredictionDisplay";
import { Provider } from "./components/ui/provider";
import { WebcamFeed } from "./components/WebcamFeed";
import { useHandTracking } from "./hooks/useHandTracking";

export const App = (): React.ReactElement => {
  const { videoRef, prediction } = useHandTracking();
  return (
    <Provider>
      <MainLayout>
        <Flex
          flexDirection="column"
          alignItems="center"
          justifyContent="center"
          gap={4}
        >
          <WebcamFeed videoRef={videoRef} />
          {/* <PredictionDisplay prediction={prediction} /> */}
        </Flex>
      </MainLayout>
    </Provider>
  );
};
