"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const vscode = require("vscode");
function activate(context) {
    const provider = vscode.languages.registerCompletionItemProvider('epp', {
        provideCompletionItems(document, position) {
            const keywords = [
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
    }, ' ', '\n');
    context.subscriptions.push(provider);
}
exports.activate = activate;
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map