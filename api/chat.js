export default async function handler(req, res) {
    if (req.method !== 'POST') return res.status(405).send('Method Not Allowed');

    // This pulls from the secret vault we will set up in Vercel
    const KEY = process.env.GEMINI_KEY; 
    const { prompt } = req.body;

    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${KEY}`;

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                contents: [{ parts: [{ text: prompt }] }]
            })
        });
        
        const data = await response.json();
        const aiReply = data?.candidates?.[0]?.content?.parts?.[0]?.text || "No response.";
        
        res.status(200).json({ reply: aiReply });
    } catch (error) {
        res.status(500).json({ error: "Server Error" });
    }
}
