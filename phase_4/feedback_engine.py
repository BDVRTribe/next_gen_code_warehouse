# phase_4/feedback_engine.py

__all__ = ["FeedbackEngine"]

class FeedbackEngine:
    def __init__(self):
        self.q_table = {}  # Maps (state, action) → reward

    def encode_state(self, goal, result, error):
        # Convert environment state to a simplified representation
        return f"{goal['goal_text']}|{result}|{bool(error)}"

    def choose_action(self, state):
        # Always mutate for now (later we can train better policies)
        return "mutate"

    def get_reward(self, score):
        # Simple reward: score is reward
        return score

    def update(self, state, action, reward):
        key = (state, action)
        self.q_table[key] = self.q_table.get(key, 0.0) + 0.1 * (reward - self.q_table.get(key, 0.0))

    def feedback(self, goal, result, error, score):
        state = self.encode_state(goal, result, error)
        action = self.choose_action(state)
        reward = self.get_reward(score)
        self.update(state, action, reward)
        return action

