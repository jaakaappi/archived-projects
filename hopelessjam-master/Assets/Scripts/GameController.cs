using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;

public class GameController : MonoBehaviour
{
    public Text ScoreText, TimerText;
    private bool gameActive;
    private int score, trapCount;
    private float startTime, spawnCooldown, lastSpawn;

    public GameObject trapParent, human, spawnPoint;
    private List<Trap> traps = new List<Trap>();
    private List<char> trapChars;


    // Start is called before the first frame update
    void Start()
    {
        score = 0;
        startTime = Time.time;
        spawnCooldown = 0.3f;
        // Save all the traps to a list
        trapCount = trapParent.transform.childCount;
        for (int i = 0; i < trapCount; i++)
        {
            traps.Add(trapParent.transform.GetChild(i).GetComponent<Trap>());
        }
    }

    // Update is called once per frame
    void Update()
    {
        if (Time.time - startTime <= 360.0f)
        {

            // UI updating
            ScoreText.text = score.ToString();
            TimerText.text = TimeParser(Time.time - startTime);

            // Spawn timer
            if (Time.time - lastSpawn > spawnCooldown)
            {
                lastSpawn = Time.time;
                SpawnHuman();
            }

            // Controls, etc
            foreach (char c in Input.inputString)
            {
                for (int i = 0; i < trapCount; i++)
                {
                    if (c == traps[i].trapChar)
                    {
                        traps[i].TrapActivation();
                    }
                }
            }
        }
        else
        {
            // Game has ended
            TimerText.text = "12:00\nNOON";
            ScoreText.text = "Your final score is\n" + score.ToString();
        }
        if (Input.GetKeyDown(KeyCode.Space))
        {
            SceneManager.LoadScene(0, LoadSceneMode.Single);
        }
    }

    private string TimeParser(float time)
    {
        float minutes = Mathf.Floor((time) / 60);
        float seconds = Mathf.Floor((time) % 60);
        float msecs = Mathf.Floor(((time) * 100) % 100);
        return ((minutes + 6).ToString() + ":" + seconds.ToString("00"));
    }

    private void SpawnHuman()
    {
        Instantiate(human, spawnPoint.transform);
    }

    public void KillHuman(GameObject human)
    {
        Destroy(human);
        IncreaseScore(1);
    }


    private void IncreaseScore(int increase)
    {
        score += increase;
    }
}