const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { OpenAI } = require('openai');
const fs = require('fs');
const csv = require('csv-parser');

const app = express();
const port = 3001;

const openai = new OpenAI();

app.use(cors());
app.use(bodyParser.json());

// Load CSV Data
const loadCSVData = () => {
  return new Promise((resolve, reject) => {
    const results = [];
    fs.createReadStream('trainingData.csv')
      .pipe(csv())
      .on('data', (data) => results.push(data))
      .on('end', () => resolve(results))
      .on('error', (error) => reject(error));
  });
};

let data;
loadCSVData().then((csvData) => {
  data = csvData;
});

app.post('/ask', async (req, res) => {
  const { question, history } = req.body;

  //Not maintainign history for now

  const prompt = `You are given the following CSV data:\n\n${JSON.stringify(
    data,
    null,
    2
  )}
  \n\nAnswer the following question based on this data: ${question}
  \n\nPlease adhere to the following guidelines when responding to the question:
  1. Provide the answer directly without referencing the source.
  2. If the CSV does not contain the answer, respond with your own answer.
  3. If the question is meant to conclude the chat, simply express thanks and end the conversation.`;

  try {
    const response = await openai.chat.completions.create({
      model: 'gpt-4',
      messages: [
        {
          role: 'user',
          content: prompt,
        },
      ],
    });

    const answer = response.choices[0].message.content;
    res.json({ answer });
  } catch (error) {
    console.error('Error asking question:', error);
    res.status(500).json({ error: 'Error generating response from OpenAI' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
