import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import ChatBoxdApp from "./ChatBoxdApp.tsx";

import "./index.css";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ChatBoxdApp />
  </StrictMode>
);
