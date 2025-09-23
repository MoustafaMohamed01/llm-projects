import 'dart:convert';
import 'dart:typed_data';
import 'package:syncfusion_flutter_pdf/pdf.dart';
import 'package:archive/archive.dart';

class DocumentProcessor {
  static Future<String> extractTextFromPDF(Uint8List pdfBytes) async {
    try {
      PdfDocument document = PdfDocument(inputBytes: pdfBytes);

      String extractedText = PdfTextExtractor(document).extractText();

      document.dispose();

      return _cleanExtractedText(extractedText);
    } catch (e) {
      throw Exception('Failed to extract text from PDF: $e');
    }
  }

  static Future<String> extractTextFromDOCX(Uint8List docxBytes) async {
    try {
      final archive = ZipDecoder().decodeBytes(docxBytes);

      ArchiveFile? documentXml;
      for (final file in archive) {
        if (file.name == 'word/document.xml') {
          documentXml = file;
          break;
        }
      }

      if (documentXml == null) {
        throw Exception('Invalid DOCX file: document.xml not found');
      }

      final xmlContent = utf8.decode(documentXml.content as List<int>);

      String extractedText = _extractTextFromXML(xmlContent);

      return _cleanExtractedText(extractedText);
    } catch (e) {
      throw Exception('Failed to extract text from DOCX: $e');
    }
  }

  static Future<String> extractTextFromDOC(Uint8List docBytes) async {
    try {
      String content = String.fromCharCodes(docBytes);

      String extractedText = content
          .replaceAll(RegExp(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\xFF]'), ' ')
          .replaceAll(RegExp(r'\s+'), ' ')
          .trim();

      if (extractedText.length < 50) {
        throw Exception(
            'Unable to extract readable text from this .doc file. Please convert to .docx format.');
      }

      return _cleanExtractedText(extractedText);
    } catch (e) {
      throw Exception('Failed to extract text from DOC: $e');
    }
  }

  static Future<String> extractTextFromRTF(Uint8List rtfBytes) async {
    try {
      String rtfContent = utf8.decode(rtfBytes);

      String extractedText = rtfContent
          .replaceAll(RegExp(r'\\[a-z]+\d*'), '') 
          .replaceAll(RegExp(r'[{}]'), '') 
          .replaceAll(RegExp(r'\\\*[^}]*}'), '')
          .replaceAll(RegExp(r'\\[^a-z]'), '') 
          .replaceAll(RegExp(r'\s+'), ' ') 
          .trim();

      return _cleanExtractedText(extractedText);
    } catch (e) {
      throw Exception('Failed to extract text from RTF: $e');
    }
  }

  static Future<String> extractPlainText(
      Uint8List textBytes, String fileName) async {
    try {
      String content = '';

      try {
        content = utf8.decode(textBytes);
      } catch (e) {
        content = String.fromCharCodes(textBytes);
      }

      return _cleanExtractedText(content);
    } catch (e) {
      throw Exception('Failed to extract text from file: $e');
    }
  }

  static Future<String> processDocument(
      Uint8List fileBytes, String fileName) async {
    String extension = fileName.toLowerCase().split('.').last;

    switch (extension) {
      case 'pdf':
        return await extractTextFromPDF(fileBytes);
      case 'docx':
        return await extractTextFromDOCX(fileBytes);
      case 'doc':
        return await extractTextFromDOC(fileBytes);
      case 'rtf':
        return await extractTextFromRTF(fileBytes);
      case 'txt':
      case 'md':
      case 'csv':
        return await extractPlainText(fileBytes, fileName);
      default:
        throw Exception('Unsupported file format: .$extension');
    }
  }

  static bool isSupportedFileType(String fileName) {
    String extension = fileName.toLowerCase().split('.').last;
    return ['pdf', 'docx', 'doc', 'rtf', 'txt', 'md', 'csv']
        .contains(extension);
  }

  static List<String> getSupportedExtensions() {
    return ['pdf', 'docx', 'doc', 'rtf', 'txt', 'md', 'csv'];
  }

  static String _cleanExtractedText(String text) {
    return text
        .replaceAll(
            RegExp(r'\n\s*\n\s*\n+'), '\n\n')
        .replaceAll(RegExp(r'[ \t]+'), ' ') 
        .replaceAll(RegExp(r'\r\n'), '\n')
        .trim();
  }

  static String _extractTextFromXML(String xmlContent) {
    RegExp textRegex = RegExp(r'<w:t[^>]*>([^<]*)</w:t>', multiLine: true);

    StringBuffer textBuffer = StringBuffer();

    for (RegExpMatch match in textRegex.allMatches(xmlContent)) {
      String text = match.group(1) ?? '';
      if (text.isNotEmpty) {
        textBuffer.write(text);
        textBuffer.write(' ');
      }
    }

    String result = textBuffer.toString();
    result = result.replaceAll(RegExp(r'</w:p>'), '\n');

    return result;
  }

  static String getFileTypeDescription(String fileName) {
    String extension = fileName.toLowerCase().split('.').last;

    switch (extension) {
      case 'pdf':
        return 'PDF Document';
      case 'docx':
        return 'Word Document (DOCX)';
      case 'doc':
        return 'Word Document (DOC)';
      case 'rtf':
        return 'Rich Text Format';
      case 'txt':
        return 'Text File';
      case 'md':
        return 'Markdown File';
      case 'csv':
        return 'CSV File';
      default:
        return 'Unknown File Type';
    }
  }
}
