import 'dart:convert';
import 'package:http/http.dart' as http;

class GeminiService {
  static const String _apiKey = 'YOUR_GEMINI_API_KEY';
  static const String _baseUrl =
      'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent';

  Future<String> generateResponse(String prompt,
      {String? systemInstruction}) async {
    if (_apiKey == 'YOUR_GEMINI_API_KEY_HERE') {
      await Future.delayed(const Duration(seconds: 1));
      return _getMockResponse(prompt);
    }

    try {
      final requestBody = {
        'contents': [
          {
            'parts': [
              {
                'text': systemInstruction != null
                    ? '$systemInstruction\n\n$prompt'
                    : prompt
              }
            ]
          }
        ],
        'generationConfig': {
          'temperature': 0.9,
          'topK': 1,
          'topP': 1,
          'maxOutputTokens': 8192,
        },
        'safetySettings': [
          {
            'category': 'HARM_CATEGORY_HARASSMENT',
            'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
          },
          {
            'category': 'HARM_CATEGORY_HATE_SPEECH',
            'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
          },
          {
            'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
            'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
          },
          {
            'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
            'threshold': 'BLOCK_MEDIUM_AND_ABOVE'
          }
        ]
      };

      final response = await http.post(
        Uri.parse('$_baseUrl?key=$_apiKey'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode(requestBody),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['candidates'] != null &&
            data['candidates'].isNotEmpty &&
            data['candidates'][0]['content'] != null) {
          return data['candidates'][0]['content']['parts'][0]['text'];
        } else {
          throw Exception('Invalid response format from Gemini API');
        }
      } else {
        throw Exception(
            'API request failed: ${response.statusCode} ${response.reasonPhrase}');
      }
    } catch (e) {
      throw Exception('Error calling Gemini API: $e');
    }
  }

  String _getMockResponse(String prompt) {
    final responses = [
      "I understand your question about: $prompt. In a real implementation, this would connect to the Gemini API to provide detailed responses.",
      "That's an interesting point. This demo shows the UI structure, but actual AI responses would require API integration with your Gemini key.",
      "I can help with that. Please note this is a demonstration of the interface - full functionality requires your Gemini API key to be configured.",
    ];

    final hash = prompt.hashCode.abs() % responses.length;
    return responses[hash];
  }
}
