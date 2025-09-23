// Configuration - Add your Gemini API key here
const CONFIG = {
  GEMINI_API_KEY: "YOUR_GEMINI_API_KEY_HERE", // Replace with your actual API key
  GEMINI_API_URL:
    "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
  // Alternative streaming endpoint if you want streaming responses:
  // GEMINI_STREAM_URL: 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:streamGenerateContent'
};

// Global variables
let chatHistory = [];
let currentTool = "ai-assistant";
let csvData = null;
let docFile = null;

// Initialize the application
document.addEventListener("DOMContentLoaded", function () {
  setupEventListeners();

  // Check if API key is configured
  if (CONFIG.GEMINI_API_KEY === "YOUR_GEMINI_API_KEY_HERE") {
    showAlert(
      "warning",
      "Please configure your Gemini API key in the script.js file to enable AI functionality."
    );
  } else {
    showAlert(
      "success",
      "LLM Tools Suite loaded successfully with Gemini 2.5 Flash!"
    );
  }
});

function setupEventListeners() {
  // Tool navigation
  document.querySelectorAll(".tool-button").forEach((button) => {
    button.addEventListener("click", function () {
      switchTool(this.dataset.tool);
    });
  });

  // File drag and drop
  const fileUploads = document.querySelectorAll(".file-upload");
  fileUploads.forEach((upload) => {
    upload.addEventListener("dragover", handleDragOver);
    upload.addEventListener("dragleave", handleDragLeave);
    upload.addEventListener("drop", handleDrop);
  });
}

// Gemini API Integration Functions
async function callGeminiAPI(prompt, systemInstruction = null) {
  if (CONFIG.GEMINI_API_KEY === "YOUR_GEMINI_API_KEY_HERE") {
    throw new Error("Please configure your Gemini API key in script.js");
  }

  const requestBody = {
    contents: [
      {
        parts: [
          {
            text: systemInstruction
              ? `${systemInstruction}\n\n${prompt}`
              : prompt,
          },
        ],
      },
    ],
    generationConfig: {
      temperature: 0.9,
      topK: 1,
      topP: 1,
      maxOutputTokens: 8192,
    },
    safetySettings: [
      {
        category: "HARM_CATEGORY_HARASSMENT",
        threshold: "BLOCK_MEDIUM_AND_ABOVE",
      },
      {
        category: "HARM_CATEGORY_HATE_SPEECH",
        threshold: "BLOCK_MEDIUM_AND_ABOVE",
      },
      {
        category: "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        threshold: "BLOCK_MEDIUM_AND_ABOVE",
      },
      {
        category: "HARM_CATEGORY_DANGEROUS_CONTENT",
        threshold: "BLOCK_MEDIUM_AND_ABOVE",
      },
    ],
  };

  try {
    const response = await fetch(
      `${CONFIG.GEMINI_API_URL}?key=${CONFIG.GEMINI_API_KEY}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestBody),
      }
    );

    if (!response.ok) {
      const errorData = await response.text();
      console.error("API Error:", errorData);
      throw new Error(
        `API request failed: ${response.status} ${response.statusText}`
      );
    }

    const data = await response.json();

    if (data.candidates && data.candidates[0] && data.candidates[0].content) {
      return data.candidates[0].content.parts[0].text;
    } else {
      throw new Error("Invalid response format from Gemini API");
    }
  } catch (error) {
    console.error("Error calling Gemini API:", error);
    throw error;
  }
}

function switchTool(toolName) {
  // Update active button
  document
    .querySelectorAll(".tool-button")
    .forEach((btn) => btn.classList.remove("active"));
  document.querySelector(`[data-tool="${toolName}"]`).classList.add("active");

  // Hide all tool contents
  document
    .querySelectorAll(".tool-content")
    .forEach((content) => content.classList.add("hidden"));

  // Show selected tool content
  document.getElementById(toolName).classList.remove("hidden");

  currentTool = toolName;
}

function handleKeyPress(event) {
  if (event.key === "Enter") {
    sendMessage();
  }
}

async function sendMessage() {
  const input = document.getElementById("chat-input");
  const message = input.value.trim();

  if (!message) return;

  // Disable send button
  const sendButton = document.querySelector(".send-button");
  sendButton.disabled = true;
  sendButton.innerHTML = '<span class="loading"></span> Thinking...';

  // Add user message to chat
  addMessage("user", message);
  input.value = "";

  try {
    const systemInstruction =
      "You are an AI assistant designed to provide professional, accurate information. Your responses should be formal, concise, and helpful, free from bias and ambiguity, and always grammatically correct.";
    const response = await callGeminiAPI(message, systemInstruction);
    addMessage("assistant", response);
  } catch (error) {
    console.error("Error:", error);
    addMessage("assistant", `Sorry, I encountered an error: ${error.message}`);
    showAlert(
      "error",
      "Failed to get AI response. Please check your API key and try again."
    );
  } finally {
    // Re-enable send button
    sendButton.disabled = false;
    sendButton.innerHTML = "Send";
  }
}

function addMessage(role, content) {
  const chatContainer = document.getElementById("chat-container");
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${role}`;
  messageDiv.textContent = content;

  chatContainer.appendChild(messageDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  chatHistory.push({ role, content });
}

function clearChat() {
  const chatContainer = document.getElementById("chat-container");
  chatContainer.innerHTML =
    '<div class="message assistant">Hello! I\'m your AI assistant. How can I help you today?</div>';
  chatHistory = [];
}

function downloadChat() {
  const content = chatHistory
    .map(
      (msg) => `${msg.role === "user" ? "You" : "Assistant"}: ${msg.content}`
    )
    .join("\n\n");
  downloadFile("chat_history.txt", content);
}

// Blog Assistant Functions
function updateWordCount(value) {
  document.getElementById("word-count-display").textContent = value + " words";
}

async function generateBlog() {
  const title = document.getElementById("blog-title").value;
  const keywords = document.getElementById("keywords").value;
  const wordCount = document.getElementById("word-count").value;

  if (!title || !keywords) {
    showAlert("warning", "Please provide both a blog title and keywords.");
    return;
  }

  const generateButton = document.querySelector(
    "#blog-assistant .primary-button"
  );
  generateButton.disabled = true;
  generateButton.innerHTML = '<span class="loading"></span> Generating...';

  try {
    const prompt = `Generate a comprehensive, well-structured, and engaging blog post.
        **Title:** "${title}"
        **Keywords:** "${keywords}" (Integrate these naturally throughout the content)
        **Tone:** Professional yet accessible, suitable for a broad audience.
        **Structure:** Include a captivating introduction, informative body paragraphs with clear headings/subheadings, and a concise conclusion (with a call to action if appropriate).
        **Word Count:** Approximately ${wordCount} words.`;

    const response = await callGeminiAPI(prompt);

    document.getElementById("blog-content").innerHTML =
      formatMarkdown(response);
    document.getElementById("blog-output").classList.remove("hidden");

    showAlert("success", "Blog post generated successfully!");
  } catch (error) {
    console.error("Error generating blog:", error);
    showAlert("error", "Failed to generate blog post. Please try again.");
  } finally {
    generateButton.disabled = false;
    generateButton.innerHTML = "Generate Blog";
  }
}

function downloadBlog() {
  const content = document.getElementById("blog-content").textContent;
  const title =
    document.getElementById("blog-title").value.replace(/\s+/g, "_") ||
    "generated_blog";
  downloadFile(`${title}.md`, content);
}

// CSV Analyzer Functions
function handleCSVUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = function (e) {
    try {
      const csv = e.target.result;
      const lines = csv.split("\n");
      const headers = lines[0].split(",");

      // Create preview table
      let tableHTML =
        '<table style="width:100%; border-collapse: collapse; margin: 1rem 0;">';
      tableHTML += "<thead><tr>";
      headers.forEach((header) => {
        tableHTML += `<th style="border: 1px solid rgba(255,255,255,0.2); padding: 0.5rem; background: rgba(79,172,254,0.2);">${header.trim()}</th>`;
      });
      tableHTML += "</tr></thead><tbody>";

      // Show first 5 rows
      for (let i = 1; i < Math.min(6, lines.length); i++) {
        if (lines[i].trim()) {
          const cells = lines[i].split(",");
          tableHTML += "<tr>";
          cells.forEach((cell) => {
            tableHTML += `<td style="border: 1px solid rgba(255,255,255,0.2); padding: 0.5rem;">${cell.trim()}</td>`;
          });
          tableHTML += "</tr>";
        }
      }
      tableHTML += "</tbody></table>";

      document.getElementById("csv-table").innerHTML = tableHTML;
      document.getElementById("csv-preview").classList.remove("hidden");
      document.getElementById("csv-chat").classList.remove("hidden");

      csvData = { headers, lines, content: csv };
      showAlert(
        "success",
        `CSV uploaded successfully! ${lines.length - 1} rows, ${
          headers.length
        } columns.`
      );
    } catch (error) {
      showAlert(
        "error",
        "Error parsing CSV file. Please ensure it's properly formatted."
      );
    }
  };
  reader.readAsText(file);
}

function handleCSVKeyPress(event) {
  if (event.key === "Enter") {
    askCSVQuestion();
  }
}

async function askCSVQuestion() {
  const input = document.getElementById("csv-question");
  const question = input.value.trim();

  if (!question || !csvData) return;

  const chatContainer = document.getElementById("csv-chat-container");

  // Add user question
  const userMsg = document.createElement("div");
  userMsg.className = "message user";
  userMsg.textContent = question;
  chatContainer.appendChild(userMsg);

  input.value = "";

  // Add loading message
  const loadingMsg = document.createElement("div");
  loadingMsg.className = "message assistant";
  loadingMsg.innerHTML = '<span class="loading"></span> Analyzing data...';
  chatContainer.appendChild(loadingMsg);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  try {
    const csvSample = csvData.content.substring(0, 3000); // First 3000 characters
    const prompt = `You are an expert data analysis assistant. The user has provided a CSV dataset with the following columns: ${csvData.headers.join(
      ", "
    )}.

Here is a sample of the CSV data:
\`\`\`csv
${csvSample}
\`\`\`

Please answer the following question about the data professionally and provide actionable insights if applicable:

Question: ${question}`;

    const response = await callGeminiAPI(prompt);

    // Replace loading message with actual response
    loadingMsg.textContent = response;
    chatContainer.scrollTop = chatContainer.scrollHeight;
  } catch (error) {
    loadingMsg.textContent = `Error analyzing data: ${error.message}`;
    showAlert("error", "Failed to analyze data. Please try again.");
  }
}

// SQL Generator Functions
async function generateSQL() {
  const description = document.getElementById("sql-description").value;
  const context = document.getElementById("db-context").value;
  const dialect = document.getElementById("sql-dialect").value;

  if (!description) {
    showAlert("warning", "Please provide a query description.");
    return;
  }

  const generateButton = document.querySelector(
    "#sql-generator .primary-button"
  );
  generateButton.disabled = true;
  generateButton.innerHTML = '<span class="loading"></span> Generating...';

  try {
    const sqlPrompt = `Generate a ${dialect} SQL query based on the following description:
Description: ${description}
${context ? `Database Context: ${context}` : ""}
Provide only the SQL query as a raw string, without any additional explanations, markdown code block delimiters, or introductory/concluding remarks.`;

    const sqlQuery = await callGeminiAPI(sqlPrompt);

    const outputPrompt = `Given the following SQL Query:
\`\`\`sql
${sqlQuery}
\`\`\`
What would be a plausible sample tabular response?
Provide a concise sample tabular response formatted as a Markdown table, with no additional explanation.
If the query is for DDL/DML (e.g., CREATE, INSERT, UPDATE, DELETE), state "No direct tabular output for this type of query."`;

    const expectedOutput = await callGeminiAPI(outputPrompt);

    const explanationPrompt = `Explain the following SQL Query concisely and professionally:
\`\`\`sql
${sqlQuery}
\`\`\`
Focus on what the query does and its purpose.`;

    const explanation = await callGeminiAPI(explanationPrompt);

    // Clean up SQL query (remove markdown formatting if present)
    const cleanedSQL = sqlQuery
      .replace(/```sql\n?/g, "")
      .replace(/```\n?/g, "")
      .trim();

    document.getElementById("sql-query").textContent = cleanedSQL;
    document.getElementById("sql-expected-output").innerHTML =
      formatMarkdown(expectedOutput);
    document.getElementById("sql-explanation").textContent = explanation;

    document.getElementById("sql-output").classList.remove("hidden");
    showAlert("success", "SQL query generated successfully!");
  } catch (error) {
    console.error("Error generating SQL:", error);
    showAlert("error", "Failed to generate SQL query. Please try again.");
  } finally {
    generateButton.disabled = false;
    generateButton.innerHTML = "Generate SQL Query";
  }
}

function downloadSQL() {
  const query = document.getElementById("sql-query").textContent;
  const explanation = document.getElementById("sql-explanation").textContent;
  const content = `### Generated SQL Query:\n\`\`\`sql\n${query}\n\`\`\`\n\n### Explanation:\n${explanation}`;
  downloadFile("sql_query_details.md", content);
}

// Document Summarizer Functions
function handleDocumentUpload(event) {
  const file = event.target.files[0];
  if (!file) return;

  if (file.size > 20 * 1024 * 1024) {
    showAlert("warning", "File size exceeds 20MB. Processing may be slower.");
  }

  docFile = file;
  showAlert("success", `Document "${file.name}" uploaded successfully.`);
}

async function summarizeDocument() {
  if (!docFile) {
    showAlert("warning", "Please upload a document first.");
    return;
  }

  const summarizeButton = document.querySelector(
    "#document-summarizer .primary-button"
  );
  summarizeButton.disabled = true;
  summarizeButton.innerHTML = '<span class="loading"></span> Processing...';

  try {
    // For this demo, we'll simulate document processing
    // In a real implementation, you'd need to:
    // 1. Extract text from PDF/DOCX files using libraries like pdf-lib, docx, etc.
    // 2. Send the extracted text to Gemini API

    showAlert(
      "info",
      "Document processing requires server-side implementation for PDF/DOCX text extraction."
    );

    // Simulated summary
    const mockSummary = `Document Summary for "${docFile.name}":

This is a demonstration of document summarization. In a production environment, this would:

• Extract text content from PDF or Word documents using specialized libraries
• Process the extracted text through the Gemini API for intelligent summarization
• Provide key insights and main points from the document
• Handle various document formats and structures

To implement full functionality, you'll need server-side processing to extract text from documents before sending to the Gemini API.`;

    document.getElementById("doc-summary").textContent = mockSummary;
    document.getElementById("doc-output").classList.remove("hidden");
  } catch (error) {
    console.error("Error processing document:", error);
    showAlert("error", "Failed to process document. Please try again.");
  } finally {
    summarizeButton.disabled = false;
    summarizeButton.innerHTML = "Generate Summary";
  }
}

function downloadDocSummary() {
  const content = document.getElementById("doc-summary").textContent;
  downloadFile("document_summary.txt", content);
}

// Website Summarizer Functions
async function summarizeWebsite() {
  const url = document.getElementById("website-url").value;

  if (!url) {
    showAlert("warning", "Please enter a website URL.");
    return;
  }

  if (!isValidURL(url)) {
    showAlert(
      "error",
      "Please enter a valid URL starting with http:// or https://"
    );
    return;
  }

  const summarizeButton = document.querySelector(
    "#website-summarizer .primary-button"
  );
  summarizeButton.disabled = true;
  summarizeButton.innerHTML = '<span class="loading"></span> Processing...';

  try {
    // Note: Due to CORS restrictions, fetching websites directly from the browser won't work
    // This would need to be implemented on the server side
    showAlert(
      "info",
      "Website summarization requires server-side implementation to bypass CORS restrictions."
    );

    // For demo purposes, we'll generate a sample summary
    const prompt = `Based on the URL "${url}", provide a general approach for website summarization. Explain what type of content analysis would be performed if this were a real implementation.`;

    const response = await callGeminiAPI(prompt);

    document.getElementById("website-summary").innerHTML =
      formatMarkdown(response);
    document.getElementById("website-output").classList.remove("hidden");
  } catch (error) {
    console.error("Error processing website:", error);
    showAlert("error", "Failed to process website. Please try again.");
  } finally {
    summarizeButton.disabled = false;
    summarizeButton.innerHTML = "Summarize Website";
  }
}

function downloadWebsiteSummary() {
  const content = document.getElementById("website-summary").textContent;
  downloadFile("website_summary.md", content);
}

// Code Explainer Functions
async function explainCode() {
  const language = document.getElementById("code-language").value;
  const code = document.getElementById("code-input").value;

  if (!code.trim()) {
    showAlert("warning", "Please paste some code to explain.");
    return;
  }

  const explainButton = document.querySelector(
    "#code-explainer .primary-button"
  );
  explainButton.disabled = true;
  explainButton.innerHTML = '<span class="loading"></span> Analyzing...';

  try {
    const prompt = `You are a senior software engineer and code reviewer.

1. First, **print the entire ${language} code snippet exactly as provided**, clearly labeled as 'Full Code:'.

2. Then provide a **comprehensive overview explanation** of what the entire code does.

3. Finally, give a **detailed, line-by-line explanation** of the code. For each line:
   - Explain what the line does.
   - Explain each key word, function, or syntax element.
   - Use bullet points or markdown formatting for clarity.
   - Explain context if part of a block (function, loop, condition).
   - Write lines in code blocks.

Here is the code:
\`\`\`${language.toLowerCase()}
${code}
\`\`\`

Start with the full code, then overview, then line-by-line explanation.`;

    const response = await callGeminiAPI(prompt);

    document.getElementById("code-explanation").innerHTML =
      formatMarkdown(response);
    document.getElementById("code-output").classList.remove("hidden");

    showAlert("success", "Code explanation generated successfully!");
  } catch (error) {
    console.error("Error explaining code:", error);
    showAlert("error", "Failed to explain code. Please try again.");
  } finally {
    explainButton.disabled = false;
    explainButton.innerHTML = "Explain Code";
  }
}

function downloadCodeExplanation() {
  const content = document.getElementById("code-explanation").textContent;
  downloadFile("code_explanation.md", content);
}

// Utility Functions
function downloadFile(filename, content) {
  const blob = new Blob([content], { type: "text/plain" });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  window.URL.revokeObjectURL(url);
}

function formatMarkdown(text) {
  // Clean up any existing HTML first and handle special characters
  let formatted = text
    // Handle code blocks first (before other formatting)
    .replace(
      /```(\w+)?\s*\n([\s\S]*?)\n```/g,
      '<div class="code-block"><pre><code>$2</code></pre></div>'
    )
    .replace(
      /```([\s\S]*?)```/g,
      '<div class="code-block"><pre><code>$1</code></pre></div>'
    )

    // Handle inline code (before bold/italic to avoid conflicts)
    .replace(/`([^`\n]+)`/g, '<code class="inline-code">$1</code>')

    // Handle headers (use ^ for line start and $ for line end)
    .replace(/^### (.+)$/gm, "<h3>$1</h3>")
    .replace(/^## (.+)$/gm, "<h2>$1</h2>")
    .replace(/^# (.+)$/gm, "<h1>$1</h1>")

    // Handle bold and italic (be careful with order)
    .replace(/\*\*\*(.+?)\*\*\*/g, "<strong><em>$1</em></strong>")
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g, "<em>$1</em>")

    // Handle unordered lists
    .replace(/^[\*\-] (.+)$/gm, "<li>$1</li>")

    // Handle numbered lists
    .replace(/^\d+\. (.+)$/gm, "<li>$1</li>")

    // Convert double line breaks to paragraph breaks
    .replace(/\n\n+/g, "</p><p>")

    // Convert single line breaks to <br>
    .replace(/\n/g, "<br>");

  // Wrap consecutive list items in ul tags
  formatted = formatted.replace(
    /(<li>.*?<\/li>)(\s*<br>\s*<li>.*?<\/li>)*/g,
    function (match) {
      // Remove <br> tags between list items
      const cleanMatch = match.replace(/<br>\s*/g, "");
      return "<ul>" + cleanMatch + "</ul>";
    }
  );

  // Wrap content in paragraphs if it doesn't start with a block element
  if (!formatted.match(/^<(h[1-6]|div|ul|ol)/)) {
    formatted = "<p>" + formatted + "</p>";
  }

  // Clean up empty paragraphs and extra breaks
  formatted = formatted
    .replace(/<p><\/p>/g, "")
    .replace(/<p>\s*<br>\s*<\/p>/g, "")
    .replace(/(<\/h[1-6]>)\s*<br>/g, "$1")
    .replace(/(<\/ul>)\s*<br>/g, "$1")
    .replace(/(<\/div>)\s*<br>/g, "$1");

  return formatted;
}

function addMessage(role, content) {
  const chatContainer = document.getElementById("chat-container");
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${role}`;

  if (role === "assistant") {
    // Create message content with copy button
    const messageContent = document.createElement("div");
    messageContent.className = "message-content";
    messageContent.innerHTML = formatMarkdown(content);

    const copyButton = document.createElement("button");
    copyButton.className = "copy-button";
    copyButton.innerHTML = "📋 Copy";
    copyButton.onclick = () => copyToClipboard(content, copyButton);

    messageDiv.appendChild(messageContent);
    messageDiv.appendChild(copyButton);
  } else {
    messageDiv.textContent = content;
  }

  chatContainer.appendChild(messageDiv);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  chatHistory.push({ role, content });
}

function copyToClipboard(text, button) {
  navigator.clipboard
    .writeText(text)
    .then(() => {
      const originalText = button.innerHTML;
      button.innerHTML = "✅ Copied!";
      button.style.background = "rgba(46, 213, 115, 0.3)";

      setTimeout(() => {
        button.innerHTML = originalText;
        button.style.background = "";
      }, 2000);
    })
    .catch((err) => {
      console.error("Failed to copy text: ", err);
      showAlert("error", "Failed to copy to clipboard");
    });
}

function isValidURL(string) {
  try {
    new URL(string);
    return true;
  } catch (_) {
    return false;
  }
}

function showAlert(type, message) {
  // Remove existing alerts
  const existingAlerts = document.querySelectorAll(".alert");
  existingAlerts.forEach((alert) => alert.remove());

  // Create new alert
  const alert = document.createElement("div");
  alert.className = `alert ${type}`;
  alert.textContent = message;

  // Insert at the top of main content
  const mainContent = document.querySelector(".main-content");
  mainContent.insertBefore(alert, mainContent.firstChild);

  // Auto-remove after 5 seconds
  setTimeout(() => {
    alert.remove();
  }, 5000);
}

function handleDragOver(e) {
  e.preventDefault();
  e.currentTarget.classList.add("drag-over");
}

function handleDragLeave(e) {
  e.preventDefault();
  e.currentTarget.classList.remove("drag-over");
}

function handleDrop(e) {
  e.preventDefault();
  e.currentTarget.classList.remove("drag-over");

  const files = e.dataTransfer.files;
  if (files.length > 0) {
    const file = files[0];

    if (file.name.endsWith(".csv")) {
      const csvInput = document.getElementById("csv-file");
      csvInput.files = files;
      handleCSVUpload({ target: csvInput });
    } else if (file.name.endsWith(".pdf") || file.name.endsWith(".docx")) {
      const docInput = document.getElementById("doc-file");
      docInput.files = files;
      handleDocumentUpload({ target: docInput });
    }
  }
}
