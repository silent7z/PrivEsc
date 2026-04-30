# PrivEsc

Outil d'enumeration post-exploitation pour Linux. Il scanne le systeme a la recherche de vecteurs d'elevation de privileges communs.

### Fonctionnalites
- Identification du Kernel et de l'environnement.
- Recherche de binaires avec bit SUID actif.
- Detection des repertoires accessibles en ecriture pour l'injection de scripts.
- Verification des droits sur les fichiers sensibles (/etc/shadow, clés SSH).
