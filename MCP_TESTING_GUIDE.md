# 🧪 MCP Integration Testing Guide

## Quick Test Suite

### Test 1: MCP Connection ✅
```python
# After running MCP initialization cell, check for:
✅ Connected to MCP server
   Agent will now have brilliant context awareness
```

### Test 2: Basic Query (Baseline)
```python
await run_query(
    "Tell me about Samsung S24 Ultra",
    session_id="baseline_test"
)
```

**Check for**:
- 🧠 Getting intelligent context from MCP...
- ✅ MCP context injected
- Agent provides comprehensive info

---

### Test 3: The Magic Test (Follow-up Query)

**This is the KEY test that proves MCP works!**

```python
# Step 1: Initial comparison
await run_query(
    "Compare Samsung S24 Ultra and iPhone 15 Pro Max for photography",
    session_id="magic_test"
)

# Step 2: Follow-up (NO phone names mentioned!)
await run_query(
    "Which one has better battery?",
    session_id="magic_test"  # SAME session!
)
```

**Expected Behavior**:

**WITHOUT MCP** ❌:
```
Agent: "Which phones would you like me to compare?"
```

**WITH MCP** ✅:
```
Agent: "Based on our earlier comparison, Samsung S24 Ultra has 
5000mAh battery vs iPhone 15 Pro Max's 4441mAh. Samsung wins!"
```

**If you see the second response, MCP IS WORKING!** 🎉

---

### Test 4: Budget Search with Preference Learning

```python
# Query 1: Establish budget
await run_query(
    "Best phone under ₹70,000",
    session_id="budget_test"
)

# Query 2: Feature-specific (MCP remembers budget!)
await run_query(
    "Which one has the best camera?",
    session_id="budget_test"
)
```

**Expected**: Agent filters by budget from Query 1

---

### Test 5: Brand Interest Tracking

```python
# Query 1: Show interest in Samsung
await run_query(
    "Tell me about Samsung phones",
    session_id="brand_test"
)

# Query 2: General recommendation
await run_query(
    "Which phone should I buy?",
    session_id="brand_test"
)
```

**Expected**: Agent prioritizes Samsung in recommendations

---

## 🎯 Success Indicators

### ✅ MCP is Working If:
1. See "MCP context injected" for each query
2. Follow-up queries don't ask "which phones?"
3. Agent remembers previous conversation
4. Fewer clarifying questions
5. More personalized responses

### ❌ MCP Not Working If:
1. See "MCP server not available"
2. Follow-up queries ask for clarification
3. Agent doesn't remember context
4. Same behavior as basic mode

---

## 📊 Comparison Test

Run the same queries in BOTH notebooks:

### Notebook 1: `gadget_spec_scout_complete.ipynb` (Basic)
### Notebook 2: `gadget_spec_scout_mcp_enhanced.ipynb` (MCP)

**Compare**:
- Number of turns needed
- Quality of responses
- Context awareness
- User experience

---

## 🐛 Debugging

### Check MCP Logs
```python
# In Colab
!cat gadget-scout-mcp/mcp_server.log
```

### Test MCP Components Directly
```python
# Test context generation
if mcp_client:
    context = await mcp_client.get_query_context("Which phone has better battery?")
    print(context)
```

### Verify Session Continuity
```python
# Check conversation context
if mcp_client:
    conv_context = await mcp_client.read_conversation_context()
    print(json.dumps(conv_context, indent=2))
```

---

## 📈 Metrics to Track

| Test | Basic Mode | MCP Mode | Improvement |
|------|-----------|----------|-------------|
| Follow-up clarity | ❌ Asks "which phones?" | ✅ Direct answer | 100% |
| Turns per query | 2-3 | 1 | 50-66% |
| Context awareness | None | Full | ∞ |
| User satisfaction | Good | Excellent | 🚀 |

---

**The follow-up query test (#3) is the PROOF that MCP works!** ✨
