const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');

const app = express();
app.use(bodyParser.json());

app.post('/recommendMovies', (req, res) => {
  const movie1 = Number(req.body.movie1);
  const movie2 = Number(req.body.movie2);
  const languages = req.body.languages; // Get the list of selected languages
  const adult = Number(req.body.adult); // Get the "adult" flag from the request

  // Replace the Python script path with your actual Python script path
  const pythonScriptPath = '/home/pc/Desktop/Begining/webdev/HackOn/Final/Backend/LLM/python-script2.py';

  // Construct the Python command to run the script with the user's input, languages, and the "adult" flag
  const command = `python ${pythonScriptPath} ${movie1} ${movie2} ${languages.join(' ')} ${adult}`; // Pass the "adult" flag as an argument

  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing Python script: ${error}`);
      res.status(500).send('Internal Server Error');
      return;
    }

    // Assuming the Python script prints the recommendations to stdout
    const recommendations = stdout.trim().split('\n').map(Number);

    // Send the recommendations back as a JSON response
    res.json({ recommendations });
  });
});

const port = 3000;
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
