import { useEffect, useRef, useState } from "react";
import { FilesetResolver, HandLandmarker } from "@mediapipe/tasks-vision";

const SEQUENCE_LENGTH = 5;

export const useHandTracking = () => {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const [sequence, setSequence] = useState<number[][]>([]);
  const [prediction, setPrediction] = useState<string>("...");

  const lastCallTime = useRef(0);
  const handLandmarkerRef = useRef<HandLandmarker | null>(null);

  useEffect(() => {
    let animationFrameId: number;

    const init = async () => {
      const vision = await FilesetResolver.forVisionTasks(
        "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision/wasm",
      );

      const handLandmarker = await HandLandmarker.createFromOptions(vision, {
        baseOptions: {
          modelAssetPath:
            "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
        },
        runningMode: "VIDEO",
        numHands: 1,
      });

      handLandmarkerRef.current = handLandmarker;

      const video = videoRef.current!;
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
      });

      video.srcObject = stream;
      await video.play();

      const render = async () => {
        const now = performance.now();

        if (handLandmarkerRef.current && video.readyState >= 2) {
          const result = handLandmarkerRef.current.detectForVideo(video, now);

          if (result.landmarks.length > 0) {
            const hand = result.landmarks[0];

            const base = hand[0];
            const scale = Math.sqrt(
              (hand[12].x - base.x) ** 2 +
                (hand[12].y - base.y) ** 2 +
                (hand[12].z - base.z) ** 2,
            );

            const landmarks: number[] = [];

            hand.forEach((lm) => {
              landmarks.push(
                (lm.x - base.x) / scale,
                (lm.y - base.y) / scale,
                (lm.z - base.z) / scale,
              );
            });

            setSequence((prev) => {
              const updated = [...prev, landmarks];
              if (updated.length > SEQUENCE_LENGTH) updated.shift();
              return updated;
            });
          }
        }

        animationFrameId = requestAnimationFrame(render);
      };

      render();
    };

    init();

    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  useEffect(() => {
    if (sequence.length !== SEQUENCE_LENGTH) return;

    const now = Date.now();
    if (now - lastCallTime.current < 200) return;
    lastCallTime.current = now;

    const sendData = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ sequence }),
        });

        const data = await res.json();
        setPrediction(data.prediction);
      } catch (err) {
        console.error(err);
      }
    };

    sendData();
  }, [sequence]);

  return { videoRef, prediction };
};
