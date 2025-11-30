# 🚀 Running MCP Notebook with Google Drive

## ✅ You've Already Done This:
- Uploaded `gadget-scout-mcp/` folder to Google Drive
- Uploaded `mcp_client.py` to Google Drive

## 📍 Step 1: Note Your Drive Paths

Check where you uploaded the files in Google Drive. The paths will look like:

```
/content/drive/MyDrive/gadget-scout-mcp/
/content/drive/MyDrive/mcp_client.py
```

**OR** if you put them in a subfolder:
```
/content/drive/MyDrive/Colab/gadget-scout-mcp/
/content/drive/MyDrive/Colab/mcp_client.py
```

## 📝 Step 2: Upload Notebook to Colab

1. Go to https://colab.research.google.com/
2. File → Upload notebook
3. Select `gadget_spec_scout_mcp_enhanced.ipynb`

## 🔧 Step 3: Update Drive Paths

In the notebook, find this cell (Section 1.2):

```python
# Define paths (CHANGE THESE to match your Drive structure)
DRIVE_MCP_FOLDER = '/content/drive/MyDrive/gadget-scout-mcp'
DRIVE_MCP_CLIENT = '/content/drive/MyDrive/mcp_client.py'
```

**Update these paths** to match where YOU uploaded the files!

### Examples:

**If files are in root of MyDrive:**
```python
DRIVE_MCP_FOLDER = '/content/drive/MyDrive/gadget-scout-mcp'
DRIVE_MCP_CLIENT = '/content/drive/MyDrive/mcp_client.py'
```

**If files are in a "Colab" folder:**
```python
DRIVE_MCP_FOLDER = '/content/drive/MyDrive/Colab/gadget-scout-mcp'
DRIVE_MCP_CLIENT = '/content/drive/MyDrive/Colab/mcp_client.py'
```

**If files are in "Gadget Scout" folder:**
```python
DRIVE_MCP_FOLDER = '/content/drive/MyDrive/Gadget Scout/gadget-scout-mcp'
DRIVE_MCP_CLIENT = '/content/drive/MyDrive/Gadget Scout/mcp_client.py'
```

## 🔑 Step 4: Set API Key

1. Click 🔑 key icon (Secrets) in left sidebar
2. Add secret: `GEMINI_API_KEY`
3. Paste your API key
4. Enable "Notebook access"

## ▶️ Step 5: Run All Cells

1. Runtime → Run all
2. When prompted, **allow Drive access**
3. Watch for these messages:

```
Mounted at /content/drive
📦 Copying MCP files from Google Drive...
✅ Copied gadget-scout-mcp/ folder
✅ Copied mcp_client.py
✅ All MCP files copied from Google Drive!
```

Then later:
```
✅ Connected to MCP server
   Agent will now have brilliant context awareness
```

## ✨ Step 6: Test!

Run this query:

```python
await run_query(
    "Compare Samsung S24 Ultra and iPhone 15 Pro Max",
    session_id="test"
)

# Then this (no phone names!)
await run_query(
    "Which has better battery?",
    session_id="test"
)
```

**If MCP works**: Second query answers directly! 🎉

---

## 🐛 Troubleshooting

### "MCP folder not found"

**Check your path**:
```python
# Run this to see your Drive structure
!ls -la /content/drive/MyDrive/
```

Then update `DRIVE_MCP_FOLDER` to match.

### "Permission denied"

- Make sure you clicked "Connect to Google Drive" when prompted
- Re-run the Drive mount cell

### Still not working?

Set `USE_MCP = False` to use basic mode (still works!)

---

## 🎯 Benefits of Using Drive

✅ **No manual upload** - Files auto-copy from Drive  
✅ **Easy updates** - Update files in Drive, re-run notebook  
✅ **Persistent** - Files stay in Drive, not lost when Colab resets  
✅ **Shareable** - Share Drive folder with team  

---

## 📋 Quick Checklist

- [ ] Files uploaded to Google Drive
- [ ] Notebook uploaded to Colab
- [ ] Drive paths updated in notebook
- [ ] API key set in Secrets
- [ ] Run all cells
- [ ] Allow Drive access when prompted
- [ ] See "Copied from Google Drive" messages
- [ ] See "Connected to MCP server" message
- [ ] **Test follow-up query** - proves MCP works!

---

**That's it! Your MCP-enhanced notebook is ready!** 🚀
