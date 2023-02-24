import { createRoot } from "react-dom/client";
import App from "./components/App";

const appContainer = document.getElementById("app");
const root = createRoot(appContainer);

root.render(<App initialData={(window as any).initialData} />);
