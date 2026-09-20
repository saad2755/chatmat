# chatbot_engine.py
# Logique du chatbot "MathBot", basée sur nltk.chat.util (même mécanisme
# que le fichier chatbot_engine.py original, sujet remplacé par les maths).

from nltk.chat.util import Chat, reflections

PAIRS = [
    [r"mon nom est (.*)", ["Bonjour %1, ravi de faire des maths avec toi !"]],
    [r"bonjour|salut|coucou", ["Salut ! Prêt à parler de maths ?", "Bonjour, quelle question de maths as-tu ?"]],
    [r"(.*)qui es.tu(.*)|(.*)tu es qui(.*)", ["Je suis MathBot, ton assistant pour réviser les mathématiques !"]],
    [r"(.*)addition(.*)", ["L'addition combine deux nombres pour donner leur somme. Exemple : 3 + 4 = 7"]],
    [r"(.*)soustraction(.*)", ["La soustraction donne la différence entre deux nombres. Exemple : 9 - 4 = 5"]],
    [r"(.*)multiplication(.*)", ["La multiplication additionne un nombre plusieurs fois. Exemple : 3 x 4 = 12"]],
    [r"(.*)division(.*)", ["La division partage un nombre en parts égales. Exemple : 12 / 4 = 3"]],
    [r"(.*)pourcentage(.*)", ["Un pourcentage exprime une proportion sur 100. Exemple : 20% de 50 = 10"]],
    [r"(.*)racine carrée(.*)", ["La racine carrée de x est le nombre qui, multiplié par lui-même, donne x. Exemple : √16 = 4"]],
    [r"(.*)pi(.*)", ["Pi (π) est une constante mathématique qui vaut environ 3,14159, le rapport entre la circonférence et le diamètre d'un cercle"]],
    [r"(.*)pythagore(.*)", ["Le théorème de Pythagore dit que a² + b² = c² dans un triangle rectangle, où c est l'hypoténuse"]],
    [r"(.*)fraction(.*)", ["Une fraction représente une partie d'un tout, écrite sous la forme numérateur/dénominateur. Exemple : 1/2"]],
    [r"(.*)nombre premier(.*)", ["Un nombre premier n'est divisible que par 1 et lui-même. Exemples : 2, 3, 5, 7, 11, 13"]],
    [r"(.*)dérivée(.*)", ["La dérivée mesure la vitesse de variation d'une fonction. Exemple : la dérivée de x² est 2x"]],
    [r"(.*)intégrale(.*)", ["L'intégrale calcule l'aire sous une courbe. C'est l'opération inverse de la dérivée"]],
    [r"(.*)trigonométrie|(.*)sinus|(.*)cosinus|(.*)tangente(.*)", ["La trigonométrie étudie les relations entre angles et côtés d'un triangle : sinus, cosinus et tangente"]],
    [r"(.*)équation(.*)", ["Une équation est une égalité avec une inconnue à trouver. Exemple : 2x + 3 = 7, donc x = 2"]],
    [r"(.*)algèbre(.*)", ["L'algèbre utilise des lettres pour représenter des nombres inconnus dans des équations"]],
    [r"(.*)géométrie(.*)", ["La géométrie étudie les formes, les surfaces et les volumes : triangles, cercles, carrés..."]],
    [r"(.*)aire(.*)carré(.*)|(.*)aire(.*)rectangle(.*)", ["L'aire d'un rectangle est longueur x largeur. Pour un carré : côté x côté"]],
    [r"(.*)aire(.*)cercle(.*)", ["L'aire d'un cercle se calcule avec π x rayon²"]],
    [r"(.*)périmètre(.*)", ["Le périmètre est la longueur du contour d'une figure. Pour un rectangle : 2 x (longueur + largeur)"]],
    [r"(.*)euclide(.*)", ["Euclide est un mathématicien grec de l'Antiquité, surnommé le père de la géométrie"]],
    [r"(.*)al.khwarizmi(.*)", ["Al-Khwârizmî est un savant perse du IXe siècle, considéré comme le père de l'algèbre"]],
    [r"(.*)gauss(.*)", ["Carl Friedrich Gauss est un mathématicien allemand, surnommé le prince des mathématiciens"]],
    [r"(.*)euler(.*)", ["Leonhard Euler est un mathématicien suisse qui a introduit de nombreuses notations utilisées aujourd'hui, comme e et i"]],
    [r"(.*)table de multiplication(.*)", ["Je peux t'aider ! Demande-moi par exemple : 'multiplication' pour un rappel, ou entraîne-toi avec des exemples"]],
    [r"merci(.*)", ["De rien, continue à t'entraîner en maths !"]],
    [r"au revoir|bye|quitter", ["Au revoir ! Bonne continuation en mathématiques 🧮"]],
    [r"(.*)", ["Je ne comprends pas, pose-moi une question sur les mathématiques (addition, fractions, géométrie, algèbre...)"]],
]

_chat = Chat(PAIRS, reflections)


def get_response(message: str) -> str:
    """Retourne la réponse du chatbot pour un message utilisateur donné."""
    if not message or not message.strip():
        return "Pose-moi une question de mathématiques !"
    response = _chat.respond(message.strip())
    return response or "Je ne comprends pas, pose-moi une question sur les mathématiques"
