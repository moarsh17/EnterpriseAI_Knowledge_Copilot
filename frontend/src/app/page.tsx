import Sidebar from "@/components/Sidebar";
import ChatInterface from "@/components/ChatInterface";

export default function Home() {
  return (
    <main className="flex w-full h-screen overflow-hidden">
      <Sidebar />
      <ChatInterface />
    </main>
  );
}
