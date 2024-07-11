

const express = require('express');
const axios = require('axios');
const cors = require('cors');
const path = require('path'); // Added for serving static files
const app = express();
const PORT = 400; // or any other available port

// const pinterestToken = 'pina_AMAUT2AWAC7NWAQAGAAC6DRYEEEZTEABACGSOCMJJIX2LSXDKTDZTKQHBRUVLWUULFQ5TX3D4MHVEA7GG2D4DHW7DQRIXIYA';

app.use(cors()); // Enable CORS for all routes

app.use(express.json());

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// app.get('/api/pinterest-images', async (req, res) => {
//     try {
//         const response = await axios.get(`https://api.pinterest.com/v1/me/pins/?access_token=${pinterestToken}&fields=id,link,note,url,image`);
//         res.json(response.data);
//     } catch (error) {
//         console.error(error);
//         res.status(500).send('Error fetching Pinterest images');
//     }
// });

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
    console.log("not get");
});
