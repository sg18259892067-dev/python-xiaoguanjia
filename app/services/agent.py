# agent.py

class Memory:
    def load(self, user_id):
        # V0 阶段先写死用户数据
        return {
            "user_id": user_id,
            "preferences": {
                "tone": "gentle",
                "transport": "bike"
            },
            "stats": {
                "ignored_7d": 0
            }
        }


class Decision:
    def __init__(self, act, reason=""):
        self.act = act
        self.reason = reason


class DecisionEngine:
    def should_act(self, profile, event):
        # 如果最近被忽略太多次，就沉默
        if profile["stats"]["ignored_7d"] >= 3:
            return Decision(False, "too_many_ignored")

        # 如果重要性太低，不提醒
        if event["importance"] < 0.5:
            return Decision(False, "low_importance")

        return Decision(True, "worth_it")


class ExpressionEngine:
    def generate(self, profile, event, decision):
        tone = profile["preferences"]["tone"]

        if event["type"] == "weather" and event["condition"] == "rain":
            if tone == "gentle":
                return "外面可能要下雨了，带把伞会安心一点。"
            else:
                return "今天有雨。"

        return "今天记得照顾好自己。"


class Agent:
    def __init__(self):
        self.memory = Memory()
        self.decision_engine = DecisionEngine()
        self.expression_engine = ExpressionEngine()

    def handle_event(self, user_id, event):
        profile = self.memory.load(user_id)

        decision = self.decision_engine.should_act(profile, event)

        if not decision.act:
            return None

        message = self.expression_engine.generate(profile, event, decision)

        return message