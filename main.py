class LispInterpreter:
    def __init__(self):
        self.environment = {}

    def eval(self, exp):
        if isinstance(exp, int):
            return exp
        elif isinstance(exp, str):
            return self.environment.get(exp)
        elif exp[0] == '+':
            return sum(self.eval(arg) for arg in exp[1:])
        elif exp[0] == '*':
            result = 1
            for arg in exp[1:]:
                result *= self.eval(arg)
            return result
        elif exp[0] == 'lambda':
            _, params, body = exp
            return lambda *args: self.eval_lambda(body, dict(zip(params, args)))
        elif isinstance(exp, list):
            func = self.eval(exp[0])
            args = [self.eval(arg) for arg in exp[1:]]
            return func(*args)
        else:
            raise ValueError(f"Unknown expression: {exp}")

    def eval_lambda(self, body, local_env):
        saved_env = self.environment.copy()
        self.environment.update(local_env)
        try:
            return self.eval(body)
        finally:
            self.environment = saved_env

    def repl(self):
        while True:
            try:
                code = input("> ")
                if not code:
                    continue
                result = self.eval(self.parse(code))
                print(result)
            except Exception as e:
                print(f"Error: {e}")

    def parse(self, code):
        return self._parse_tokenized(self._tokenize(code))

    def _tokenize(self, code):
        return code.replace('(', ' ( ').replace(')', ' ) ').split()

    def _parse_tokenized(self, tokens):
        token = tokens.pop(0)
        if '(' == token:
            L = []
            while tokens[0] != ')':
                L.append(self._parse_tokenized(tokens))
            tokens.pop(0)  # pop off ')'
            return L
        elif ')' == token:
            raise SyntaxError('unexpected )')
        elif token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
            return int(token)
        else:
            return str(token)


if __name__ == "__main__":
    interpreter = LispInterpreter()
    interpreter.repl()
