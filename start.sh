if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/TEAM-PYRO-BOTZ/PYRO-RENAMER-PRO.git /PYRO-RENAMER-PRO     
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /PYRO-RENAMER-PRO
fi
cd /PYRO-RENAMER-PRO
pip3 install -U -r requirements.txt
echo "𝔹𝕆𝕋 𝕀𝕊 𝕊𝕋𝔸ℝ𝕋𝕀ℕ𝔾 ......"
python3 -m bot
