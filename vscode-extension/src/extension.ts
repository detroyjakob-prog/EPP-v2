import * as vscode from 'vscode';

export function activate(context: vscode.ExtensionContext) {
  const provider = vscode.languages.registerCompletionItemProvider(
    'epp',
    {
      provideCompletionItems(document: vscode.TextDocument, position: vscode.Position) {
        const keywords: vscode.CompletionItem[] = [
          new vscode.CompletionItem('say', vscode.CompletionItemKind.Keyword),
          new vscode.CompletionItem('print', vscode.CompletionItemKind.Keyword),
          new vscode.CompletionItem('let', vscode.CompletionItemKind.Keyword),
          new vscode.CompletionItem('be', vscode.CompletionItemKind.Keyword),
          new vscode.CompletionItem('if', vscode.CompletionItemKind.Keyword),
          new vscode.CompletionItem('end if', vscode.CompletionItemKind.Keyword),
          new vscode.CompletionItem('repeat', vscode.CompletionItemKind.Keyword),
          new vscode.CompletionItem('end repeat', vscode.CompletionItemKind.Keyword),
          new vscode.CompletionItem('ask', vscode.CompletionItemKind.Keyword),
          new vscode.CompletionItem('as', vscode.CompletionItemKind.Keyword),
          new vscode.CompletionItem('is', vscode.CompletionItemKind.Operator),
          new vscode.CompletionItem('is not', vscode.CompletionItemKind.Operator),
          new vscode.CompletionItem('greater than', vscode.CompletionItemKind.Operator),
          new vscode.CompletionItem('less than', vscode.CompletionItemKind.Operator),
          new vscode.CompletionItem('times', vscode.CompletionItemKind.Keyword)
        ];

        return keywords;
      }
    },
    ' ', '\n'
  );

  context.subscriptions.push(provider);
}

export function deactivate() {}