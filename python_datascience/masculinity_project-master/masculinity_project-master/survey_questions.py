'''
                                        Survey_question

It is a small code line file from the Masculinity Survey Project.
The information used to make the list of questions is found in the masculinity-survey.pdf.
The code creates and saves a survey questions pandas series.
'''
#
###########  Library
#
import pandas as pd
#
###########  Questions' reference index
#
question_num = [
    'q0001', 'q0002', 'q0004', 'q0005', # Ideas about masculinity
    'q0007_0001', 'q0007_0002', 'q0007_0003', 'q0007_0004', 'q0007_0005', # Matrix00
    'q0007_0006', 'q0007_0007', 'q0007_0008', 'q0007_0009','q0007_0010', 'q0007_0011', # Matrix
    'q0008', 'q0009', # Lifestyle
    'q0010', 'q0011', 'q0012', 'q0013', 'q0014', 'q0015', # Employment
    'q0017', 'q0018', 'q0019', 'q0020', 'q0021', 'q0022', # Relationships
    'q0024', 'q0025', 'q0026', 'q0028', 'q0029', 'q0030', 'q0034', 'q0035', 'q0036' # Demographics
]
#
###########  Questions
#
questions = [
# Ideas about masculinity
    'In general, how masculine or “manly” do you feel?',
    'How important is it to you that others see you as masculine?',
    'Where have you gotten your ideas about what it means to be a good man?',
    'Do you think that society puts pressure on men in a way that is unhealthy or badfor them?',
# Matrix question 7
    'Ask a friend for professional advice',
    'Ask a friend for personal advice',
    'Express physical affection to male friends, like hugging, rubbing shoulders',
    'Cry',
    'Get in a physical fight with another person',
    'Have sexual relations with women, including anything from kissing to sex',
    'Have sexual relations with men, including anything from kissing to sex',
    'Watch sports of any kind',
    'Work out',
    'See a therapist',
    'Feel lonely or isolated',
# Lifestyle
    'Which of the following do you worry about on a daily or near daily basis?',
    'Which of the following categories best describes your employment status?',
# Employment
    'In which of the following ways would you say it’s an advantage to be a man at your work right now?',
    'In which of the following ways would you say it’s a disadvantage to be a man at your work right now?',
    'Have you seen or heard of a sexual harassment incident at your work? If so, how did you respond?',
    'And which of the following is the main reason you did not respond?',
    'How much have you heard about the #MeToo movement?',
    'As a man, would you say you think about your behavior at work differently in the wake of #MeToo?',
# Relationships
    'Do you typically feel as though you’re expected to make the first move in romantic relationships?',
    'How often do you try to be the one who pays when on a date?',
    'Which of the following are reasons why you try to pay when on a date?',
    'When you want to be physically intimate with someone, how do you gauge their interest?',
    'Over the past 12 months, when it comes to sexual boundaries, which of the following things have you done?',
    'Have you changed your behavior in romantic relationships in the wake of #MeToo movement?',
# Demographics
    'Are you now married, widowed, divorced, separated, or have you neverbeen married?',
    'Do you have any children?',
    'Would you describe your sexual orientation as:',
    'Are you:',
    'What is the last grade of school you completed?',
    'State',
    'Income',
    'Time Zone',
    'Device'
]
#
###########  Series
#
survey_questions = pd.Series(questions, index=question_num, name='Survey Questions')
survey_questions.to_csv('data/survey_questions.csv')
print(survey_questions)
