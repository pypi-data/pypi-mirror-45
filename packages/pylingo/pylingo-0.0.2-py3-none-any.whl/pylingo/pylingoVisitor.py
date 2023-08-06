
 #  Copyright 2019  Dialect Software LLC or its affiliates. All Rights Reserved.
 #
 #  Licensed under the MIT License (the "License").
 #
 #  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 #  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 #  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 #  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 #  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 #  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 #  SOFTWARE.
 
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .pylingoParser import pylingoParser
else:
    from pylingoParser import pylingoParser

# This class defines a complete generic visitor for a parse tree produced by pylingoParser.

class pylingoVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by pylingoParser#lexee.
    def visitLexee(self, ctx:pylingoParser.LexeeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pylingoParser#decl.
    def visitDecl(self, ctx:pylingoParser.DeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pylingoParser#comment.
    def visitComment(self, ctx:pylingoParser.CommentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pylingoParser#code.
    def visitCode(self, ctx:pylingoParser.CodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pylingoParser#preamble.
    def visitPreamble(self, ctx:pylingoParser.PreambleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pylingoParser#object.
    def visitObject(self, ctx:pylingoParser.ObjectContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pylingoParser#body.
    def visitBody(self, ctx:pylingoParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pylingoParser#variable.
    def visitVariable(self, ctx:pylingoParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pylingoParser#assignment.
    def visitAssignment(self, ctx:pylingoParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pylingoParser#array.
    def visitArray(self, ctx:pylingoParser.ArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pylingoParser#doc.
    def visitDoc(self, ctx:pylingoParser.DocContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pylingoParser#json.
    def visitJson(self, ctx:pylingoParser.JsonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pylingoParser#ident.
    def visitIdent(self, ctx:pylingoParser.IdentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by pylingoParser#value.
    def visitValue(self, ctx:pylingoParser.ValueContext):
        return self.visitChildren(ctx)



del pylingoParser