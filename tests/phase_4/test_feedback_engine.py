from phase_4.feedback_engine import FeedbackEngine

def test_feedback_engine_learning():
    engine = FeedbackEngine()
    goal = {"goal_text": "Print Hello World"}
    result = "Hello World"
    error = None
    score = 1.0

    action = engine.feedback(goal, result, error, score)
    assert action == "mutate"  # Initial default action

    assert len(engine.q_table) == 1
    for (state, act), reward in engine.q_table.items():
        expected_q = 0.1 * (score - 0)  # alpha * (reward - initial_Q)
        assert abs(reward - expected_q) < 1e-5

