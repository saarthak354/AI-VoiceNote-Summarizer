from intent import extract_intent

text = """
I really don’t like how unprepared I felt in today’s meeting.
I should probably email the team lead tomorrow and ask for clearer expectations.
"""

print(extract_intent(text))