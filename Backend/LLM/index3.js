const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');
const cors = require('cors'); // Import the cors middleware

const app = express();

// Enable CORS for all routes
app.use(cors());

app.use(bodyParser.json());

app.post('/recommendMovies', (req, res) => {
  console.log("API called");
  const movie1 = Number(req.body.movie1);
  const movie2 = Number(req.body.movie2);
  const languages = req.body.languages; // Get the list of selected languages
  console.log(movie1,movie2);
  console.log(req.body.adult);

  // Replace the Python script path with your actual Python script path
  const pythonScriptPath = '/home/pc/Desktop/Begining/webdev/HackOn/Final/Backend/LLM/python_script3.py';

  // Construct the Python command to run the script with the user's input and languages
  const command = `python ${pythonScriptPath} ${movie1} ${movie2} ${languages.join(' ')}`; // Pass the languages as space-separated values

  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error}`);
      res.status(500).send('Internal Server Error');
      return;
    }

    // Parse the Python script's response
    const recommendations = stdout.trim().split('\n').map(line => {
      const [id, poster_url] = line.split(',');
      return { id: id, poster_url: poster_url };
    });

    // Send the modified data as a JSON response
    res.json({ recommendations: recommendations });
  });
});

const port = 8000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
