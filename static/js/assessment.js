
document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const questionsContainer = document.getElementById('questions-container');
    const assessmentForm = document.getElementById('assessment-form');
    const progressBarInner = document.getElementById('progress-bar-inner');
    const progressText = document.getElementById('progress-text');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const submitBtn = document.getElementById('submit-btn');

    // --- State ---
    let currentPage = 1;
    const questionsPerPage = 25;
    const userResponses = JSON.parse(localStorage.getItem('mcmi_responses')) || {};

    const questions = [
        "I like mechanics magazines",
        "I have a good appetite",
        "I wake up fresh and rested most mornings",
        "I think I would like the work of a librarian",
        "I am easily awakened by noise",
        "I like to read newspaper articles on crime",
        "My hands and feet are usually warm enough",
        "My daily life is full of things that keep me interested",
        "I am about as able to work as I ever was",
        "There seems to be a lump in my throat much of the time",
        "A person should try to understand his dreams and be guided by or take warning from them",
        "I enjoy detective or mystery stories",
        "I work under a great deal of tension",
        "I have diarrhea once a month or more",
        "Once in a while I think of things too bad to talk about",
        "I am sure I get a raw deal from life",
        "My father was a good man",
        "I am very seldom troubled by constipation",
        "At times I have very much wanted to leave home",
        "My sex life is satisfactory",
        "At times I have fits of laughing and crying that I cannot control",
        "Evil spirits possess me at times",
        "I am troubled by attacks of nausea and vomiting",
        "No one seems to understand me",
        "I would like to be a singer",
        "I feel that it is certainly best to keep my mouth shut when I'm in trouble",
        "I have very few headaches",
        "I should like to belong to several clubs or lodges",
        "At times I feel like smashing things",
        "I am bothered by acid stomach several times a week",
        "At times I have a strong urge to do something harmful or shocking",
        "I have nightmares every few nights",
        "I find it hard to keep my mind on a task or job",
        "I have had very peculiar and strange experiences",
        "I have a cough most of the time",
        "If people had not had it in for me, I would have been much more successful",
        "I seldom worry about my health",
        "I have never been in trouble because of my sex behavior",
        "During one period when I was a youngster, I engaged in petty thievery",
        "At times I feel like picking a fist fight with someone",
        "Much of the time my head seems to hurt all over",
        "I have had periods of days, weeks, or months when I couldn't take care of things",
        "My sleep is fitful and disturbed",
        "Much of the time I feel as if I have done something wrong or evil",
        "I am a very sociable person",
        "My judgment is better than it ever was",
        "Once a week or oftener I feel suddenly hot all over, without apparent cause",
        "When I am with people, I am bothered by hearing very queer things",
        "It would be better if almost all laws were thrown away",
        "My soul sometimes leaves my body",
        "I am in just as good physical health as most of my friends",
        "I prefer to pass by school friends, or people I know but have not seen for a long time",
        "A minister can cure disease by praying and putting his hand on your head",
        "I am liked by most people who know me",
        "I am almost never bothered by pains over the heart or in my chest",
        "As a youngster I was suspended from school one or more times for cutting up",
        "I believe I am being plotted against",
        "I wish I were not bothered by thoughts about sex",
        "I have often had to take orders from someone who did not know as much as I did",
        "I do not read every editorial in the newspaper every day",
        "I have not lived the right kind of life",
        "What others think of me does not bother me",
        "I have had periods in which I carried on activities without knowing later what I had been doing",
        "I believe I am being followed",
        "I like to study and read about things that I am working at",
        "I have often wished I were a girl (Or if you are a girl) I have never been sorry that I am a girl",
        "These days I find it hard not to give up hope of amounting to something",
        "I am certainly lacking in self-confidence",
        "I believe my sins are unpardonable",
        "I like to let people know where I stand on things",
        "I have periods of such great restlessness that I cannot sit long in a chair",
        "I think I would like the work of a building contractor",
        "Most of the time I feel blue",
        "I have little or no trouble with my muscles twitching or jumping",
        "I think Lincoln was greater than Washington",
        "I get mad easily and then get over it soon",
        "Most people will use somewhat unfair means to gain profit or an advantage",
        "I am troubled by discomfort in the pit of my stomach every few days or oftener",
        "I am an important person",
        "I have sometimes stayed away from another person because I feared I might do something I might regret",
        "I believe I am a condemned person",
        "I like poetry",
        "I get all the sympathy I should",
        "Sometimes when I am not feeling well I am cross",
        "I have very few fears compared to my friends",
        "I believe women ought to have as much sexual freedom as men",
        "My feelings are not easily hurt",
        "I think I would like the work of a dress designer",
        "One or more members of my family are very nervous",
        "I am worried about sex matters",
        "I have been quite independent and free from family rule",
        "I have never been in trouble with the law",
        "Sometimes I put off until tomorrow what I ought to do today",
        "I do not mind being made fun of",
        "I would like to be an auto racer",
        "My mother was a good woman",
        "If given the chance I would do something of great benefit to the world",
        "I enjoy reading love stories",
        "I am against giving money to beggars",
        "I have been inspired to a program of life based on duty",
        "I believe my home life is as pleasant as that of most people I know",
        "I am happy most of the time",
        "Lightning scares me",
        "I think most people would lie to get ahead",
        "Someone has it in for me",
        "I have strange and peculiar thoughts",
        "I believe there is a Devil and a Hell in afterlife",
        "Most people are honest chiefly through fear of being caught",
        "I have a daydream life about which I do not tell other people",
        "I wish I could be as happy as others seem to be",
        "If I were a reporter on a newspaper, I would very much like to report news of the theater",
        "I pray several times every week",
        "I have met problems so full of possibilities that I have been unable to make up my mind",
        "I do not blame a person for taking advantage of someone who lays himself open to it",
        "I have had some very unusual religious experiences",
        "I do not have a great fear of snakes",
        "I like to go to parties and other affairs where there is lots of loud fun",
        "I think I would like the work of a librarian",
        "I believe there is a God",
        "Everything is turning out just like the prophets of the Bible said it would",
        "I enjoy the excitement of a crowd",
        "My mother or father often made me obey even when I thought that it was unreasonable",
        "At parties I am more likely to sit by myself or with just one other person",
        "I am bothered by people outside, on streetcars, in stores, etc., watching me",
        "I have had no difficulty in starting or holding my bowel movement",
        "I like to flirt",
        "I believe I am no more nervous than most others",
        "I have never felt better in my life than I do now",
        "I think I would like the work of a clerk in a large department store",
        "I am easily embarrassed",
        "Most people inwardly dislike putting themselves out to help other people",
        "I like tall women",
        "I very much like hunting",
        "I have never done anything dangerous for the thrill of it",
        "I am sure I am being talked about",
        "I have periods in which I feel unusually cheerful without any special reason",
        "If I were an artist I would like to draw flowers",
        "Something exciting will almost always pull me out of it when I am feeling low",
        "I have been disappointed in love",
        "I am inclined to take things hard",
        "I have never vomited blood or coughed up blood",
        "People often disappoint me",
        "It takes a lot of argument to convince most people of the truth",
        "I have been afraid of things or people that I knew could not hurt me",
        "Most nights I go to sleep without thoughts or ideas bothering me",
        "My way of doing things is apt to be misunderstood by others",
        "I have never had a fit or convulsion",
        "I am neither gaining nor losing weight",
        "I have never been paralyzed or had any unusual weakness of any of my muscles",
        "Sometimes I have the same dream over and over",
        "I think I would like the work of a forest ranger",
        "I am afraid of using a knife or anything very sharp or pointed",
        "I have had attacks in which I could not control my movements or speech",
        "The man who provides temptation by leaving valuable property unprotected is about as much to blame",
        "I know who is responsible for most of my troubles",
        "A large number of people are guilty of bad sexual conduct",
        "I have often lost out on things because I couldn't make up my mind soon enough",
        "Sometimes I enjoy hurting persons I love",
        "I am fascinated by fire",
        "I have often felt guilty because I have pretended to feel more sorry about something",
        "What others think of me does not bother me",
        "I have never been made especially nervous over trouble that any members of my family have gotten into",
        "I am made nervous by certain animals",
        "It is all right to get around the law if you don't actually break it",
        "I have never had any breaking out on my skin that has worried me",
        "I am often said to be hotheaded",
        "I have reason for feeling jealous of one or more members of my family",
        "Most people make friends because friends are likely to be useful to them",
        "I hardly ever feel pain in the back of the neck",
        "I do not often notice my ears ringing or buzzing",
        "I have never felt better in my life than I do now",
        "I am not unusually self-conscious",
        "I have never had a fainting spell",
        "I seldom or never have dizzy spells",
        "I have had no difficulty in keeping my balance in walking"
    ];
    const totalQuestions = questions.length;

    function renderCurrentPage() {
        questionsContainer.innerHTML = '';
        const start = (currentPage - 1) * questionsPerPage;
        const end = start + questionsPerPage;
        const questionsToRender = questions.slice(start, end);

        questionsToRender.forEach((q, i) => {
            const questionIndex = start + i;
            const questionElement = document.createElement('div');
            questionElement.classList.add('question');

            const savedAnswer = userResponses[questionIndex + 1];
            const isTrueChecked = savedAnswer === true ? 'checked' : '';
            const isFalseChecked = savedAnswer === false ? 'checked' : '';

            // Updated HTML structure for single-line layout
            questionElement.innerHTML = `
                <p class="question-text">${questionIndex + 1}. ${q}</p>
                <div class="options-group">
                    <label><input type="radio" name="q${questionIndex}" value="true" ${isTrueChecked}> True</label>
                    <label><input type="radio" name="q${questionIndex}" value="false" ${isFalseChecked}> False</label>
                </div>
            `;
            questionsContainer.appendChild(questionElement);
        });
        updatePaginationControls();
        window.scrollTo(0, 0);
    }

    function updatePaginationControls() {
        const totalPages = Math.ceil(totalQuestions / questionsPerPage);
        prevBtn.disabled = currentPage === 1;
        nextBtn.disabled = currentPage === totalPages;
        
        if (currentPage === totalPages) {
            nextBtn.style.display = 'none';
            submitBtn.style.display = 'block';
        } else {
            nextBtn.style.display = 'block';
            submitBtn.style.display = 'none';
        }
    }

    function updateProgress() {
        const answeredCount = Object.keys(userResponses).length;
        const progress = (answeredCount / totalQuestions) * 100;
        progressBarInner.style.width = `${progress}%`;
        progressText.textContent = `${Math.round(progress)}% Complete`;
    }

    function handleNavigation(direction) {
        currentPage += direction;
        renderCurrentPage();
    }

    prevBtn.addEventListener('click', () => handleNavigation(-1));
    nextBtn.addEventListener('click', () => handleNavigation(1));

    assessmentForm.addEventListener('input', (e) => {
        if (e.target.type === 'radio') {
            const questionIndex = parseInt(e.target.name.substring(1)) + 1;
            userResponses[questionIndex] = e.target.value === 'true';
            localStorage.setItem('mcmi_responses', JSON.stringify(userResponses));
            updateProgress();
        }
    });

    assessmentForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const isLoggedIn = assessmentForm.dataset.isLoggedIn === 'true';

        if (!isLoggedIn) {
            alert('You must be logged in to submit the assessment. Your progress has been saved in this browser.');
            window.location.href = '/login';
            return;
        }

        if (Object.keys(userResponses).length !== totalQuestions) {
            alert('Please answer all questions before submitting.');
            return;
        }

        try {
            const response = await fetch('/api/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ responses: userResponses })
            });
            const result = await response.json();
            if (response.ok) {
                localStorage.removeItem('mcmi_responses');
                window.location.href = `/results/${result.session_id}`;
            } else {
                alert(`Error: ${result.error}`);
            }
        } catch (error) {
            console.error('Error submitting assessment:', error);
            alert('An unexpected error occurred. Please try again.');
        }
    });

    renderCurrentPage();
    updateProgress();
});
