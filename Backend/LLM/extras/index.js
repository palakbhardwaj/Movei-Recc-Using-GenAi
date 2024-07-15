const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const cors = require('cors'); // Import the cors middleware


const app = express();

// Enable CORS for all routes
app.use(cors());

app.use(bodyParser.json());

app.post('/recommendMovies', (req, res) => {
  console.log("Api called");
  const movie1 = Number(req.body.movie1);
  const movie2 = Number(req.body.movie2);
  const languages = req.body.languages; // Get the list of selected languages

  // Replace the Python script path with your actual Python script path
  const pythonScriptPath = '/home/pc/Desktop/Begining/webdev/HackOn/Final/Backend/LLM/python_script.py';

  // Construct the Python command to run the script with the user's input and languages
  const command = `python ${pythonScriptPath} ${movie1} ${movie2} ${languages.join(' ')}`; // Pass the languages as space-separated values

  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error}`);
      res.status(500).send('Internal Server Error');
      return;
    }

    // Assuming the Python script prints the poster URLs to stdout
    const posterUrls = stdout.trim().split('\n');

    // Remove the top 6 null values
    const filteredPosterUrls = posterUrls.slice(6);

    // Send the filtered poster URLs back as a JSON response
    res.json({ recommendations: filteredPosterUrls });
  });
});

const port = 8000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
