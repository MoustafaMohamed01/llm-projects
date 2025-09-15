import 'dart:convert';
import 'package:http/http.dart' as http;
import '../utils/constants.dart';

class GeminiService {
  static Future<String> generateResponse(String message) async {
    try {
      final response = await http.post(
        Uri.parse('${Constants.geminiApiUrl}?key=${Constants.geminiApiKey}'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'contents': [
            {
              'parts': [
                {
                  'text': message,
                }
              ]
            }
          ],
          'generationConfig': {
            'temperature': 0.7,
            'topK': 40,
            'topP': 0.95,
            'maxOutputTokens': 1024,
          },
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        if (data['candidates'] != null && data['candidates'].isNotEmpty) {
          return data['candidates'][0]['content']['parts'][0]['text'] ??
              'Sorry, I couldn\'t generate a response.';
        }
      }

      return 'Sorry, I encountered an error. Please try again.';
    } catch (e) {
      return 'Network error. Please check your connection and try again.';
    }
  }
}
