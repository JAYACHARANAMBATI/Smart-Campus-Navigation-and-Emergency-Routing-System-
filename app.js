const express = require("express");
const http = require("http");
const socketio = require("socket.io");
const path = require("path");

const app = express();
const server = http.createServer(app);
const io = socketio(server);

// Serve static files from the "public" directory
app.use(express.static(path.join(__dirname, "public")));

// Set EJS as the template engine
app.set("view engine", "ejs");

// Handle socket connections
io.on("connection", (socket) => {
    console.log("A user connected");

    // Handle location data from clients
    socket.on("send-location", (data) => {
        io.emit("receive-location", { id: socket.id, ...data });
    });

    // Example of emitting initial data to the client
    socket.emit("locationUpdate", { latitude: 51.505, longitude: -0.09 });

    // Handle user disconnecting
    socket.on("disconnect", () => {
        console.log("A user disconnected");
    });
});

// Serve the main page
app.get("/", (req, res) => {
    res.render("index");
});

// Start the server
server.listen(3000, () => {
    console.log("Server is running on http://localhost:3000");
});
