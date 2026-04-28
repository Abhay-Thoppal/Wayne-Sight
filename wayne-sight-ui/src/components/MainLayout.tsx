import React, { useState } from "react";
import {
  Box,
  VStack,
  HStack,
  Text,
  Image,
  IconButton,
  useDisclosure,
} from "@chakra-ui/react";

import { FiMenu, FiHome, FiSettings } from "react-icons/fi";

interface IMainLayouProps {
  children?: React.ReactNode | React.ReactNode[];
}
export const MainLayout = ({
  children,
}: IMainLayouProps): React.ReactElement => {
  const { open, onOpen, onClose } = useDisclosure();

  const [collapsed, setCollapsed] = useState(false);

  const toggleSidebar = () => setCollapsed((prev) => !prev);

  const navItems = [
    {
      label: "Home",
      icon: FiHome,
    },
    {
      label: "Settings",
      icon: FiSettings,
    },
  ];

  return (
    <Box display="flex" minH="100vh" bg="gray.950" color="white">
      <IconButton
        aria-label="Open Menu"
        display={{ base: "flex", md: "none" }}
        position="fixed"
        top={4}
        left={4}
        zIndex={100}
        onClick={onOpen}
        bg="gray.900"
        _hover={{ bg: "gray.800" }}
      >
        <FiMenu />
      </IconButton>

      <Box
        display={{ base: "none", md: "flex" }}
        flexDirection="column"
        bg="gray.900"
        border={"none"}
        transition="all 0.25s ease"
        w={collapsed ? "88px" : "260px"}
        minH="100vh"
        p={4}
        position="sticky"
        top={0}
      >
        <VStack align="stretch" gap={4} h="full">
          <HStack
            justify={collapsed ? "center" : "flex-start"}
            align="center"
            overflow="hidden"
          >
            <Image
              src="/AppIcon.png"
              alt="Wayne Sight"
              w={10}
              h={10}
              objectFit="contain"
              cursor="pointer"
              onClick={toggleSidebar}
            />
            {!collapsed && (
              <Text
                fontSize="lg"
                fontWeight="700"
                letterSpacing="tight"
                whiteSpace="nowrap"
              >
                Wayne Sight
              </Text>
            )}
          </HStack>
          <VStack align="stretch" gap={2} mt={4}>
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <HStack
                  key={item.label}
                  p={3}
                  borderRadius="lg"
                  cursor="pointer"
                  transition="all 0.2s"
                  _hover={{
                    bg: "gray.800",
                    transform: "translateX(2px)",
                  }}
                  justify={collapsed ? "center" : "flex-start"}
                >
                  <Box fontSize="20px">
                    <Icon />
                  </Box>

                  {!collapsed && (
                    <Text fontSize="sm" fontWeight="500">
                      {item.label}
                    </Text>
                  )}
                </HStack>
              );
            })}
          </VStack>

          <Box
            p={3}
            borderRadius="lg"
            bg="gray.800"
            border="1px solid"
            borderColor="gray.700"
          >
            {collapsed ? (
              <Text textAlign="center" fontSize="xs">
                👁️
              </Text>
            ) : (
              <>
                <Text fontSize="xs" color="gray.400">
                  Wayne Sight
                </Text>

                <Text fontSize="sm" fontWeight="600" mt={1}>
                  v1.0
                </Text>
              </>
            )}
          </Box>
        </VStack>
      </Box>

      <Box flex={1} p={{ base: 6, md: 8 }} overflowY="auto">
        <Text fontSize="3xl" fontWeight="700" mb={6}>
          Wayne Sight
        </Text>

        {children && (
          <VStack align="stretch" gap={4}>
            {children}
          </VStack>
        )}
      </Box>
    </Box>
  );
};
