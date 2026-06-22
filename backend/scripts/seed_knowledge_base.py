import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.session import AsyncSessionLocal
from app.models.knowledge_chunk import KnowledgeChunk
from app.services.embedding_service import generate_embedding


SEED_DATA = [
    # ── Amazon (existing) ──
    {
        "content": "Amazon SDE role requires strong CS fundamentals: data structures, algorithms, OOP design, and system design basics. Candidates are expected to write clean, working code under time pressure.",
        "source": "job_description",
        "company": "Amazon",
    },
    {
        "content": "Amazon interview experience: First round was 2 DSA questions on arrays and trees, medium difficulty on LeetCode scale. Interviewer focused heavily on time/space complexity tradeoffs.",
        "source": "interview_experience",
        "company": "Amazon",
    },
    {
        "content": "Amazon interview experience: Behavioral round followed the Leadership Principles closely. Questions like 'Tell me about a time you disagreed with a decision' and 'Describe a time you took ownership of a problem.'",
        "source": "interview_experience",
        "company": "Amazon",
    },
    {
        "content": "Amazon OA question: Given an array of integers, find the maximum sum of a contiguous subarray. Classic Kadane's algorithm problem.",
        "source": "oa_question",
        "company": "Amazon",
    },
    {
        "content": "Amazon OA question: Design a rate limiter that allows N requests per IP address per minute. Discuss the data structure choice and edge cases.",
        "source": "oa_question",
        "company": "Amazon",
    },
    {
        "content": "Amazon SDE interview commonly covers DBMS topics: normalization, ACID properties, indexing strategies, and SQL query optimization.",
        "source": "oa_question",
        "company": "Amazon",
    },

    # ── Google ──
    {
        "content": "Google SWE interviews emphasize algorithmic problem-solving, clean code, and the ability to discuss multiple approaches with clear tradeoff analysis before coding. Strong CS fundamentals and Big-O reasoning are expected at every stage.",
        "source": "job_description",
        "company": "Google",
    },
    {
        "content": "Google interview experience: Candidates report 4-5 rounds of pure coding interviews (no separate system design for new grads), each 45 minutes, focusing on graphs, trees, and dynamic programming.",
        "source": "interview_experience",
        "company": "Google",
    },
    {
        "content": "Google interview experience: The 'Googleyness' behavioral round asks about collaboration, handling ambiguity, and learning from failure, with less rigid structure than Amazon's Leadership Principles.",
        "source": "interview_experience",
        "company": "Google",
    },
    {
        "content": "Google OA question: Given a list of intervals, merge all overlapping intervals and return the result sorted by start time.",
        "source": "oa_question",
        "company": "Google",
    },
    {
        "content": "Google OA question: Implement an LRU cache with O(1) get and put operations, discussing the combination of a hash map and doubly linked list.",
        "source": "oa_question",
        "company": "Google",
    },
    {
        "content": "Google interviews frequently test on trie data structures, graph traversal (BFS/DFS), and binary search variations applied to non-trivial problems.",
        "source": "topic_focus",
        "company": "Google",
    },

    # ── Microsoft ──
    {
        "content": "Microsoft SDE interviews balance DSA with practical engineering judgment -- candidates are expected to write production-quality code, not just pass test cases, and discuss testing strategy.",
        "source": "job_description",
        "company": "Microsoft",
    },
    {
        "content": "Microsoft interview experience: Rounds typically include 1-2 DSA rounds, 1 system design round even for new grads, and a 'As Appropriate' (AA) round with a senior engineer focused on culture fit.",
        "source": "interview_experience",
        "company": "Microsoft",
    },
    {
        "content": "Microsoft interview experience: A common question style is 'design and code' -- e.g. design a parking lot system or an elevator system, then implement core classes in code during the same session.",
        "source": "interview_experience",
        "company": "Microsoft",
    },
    {
        "content": "Microsoft OA question: Implement a basic version of a text editor's undo/redo functionality using two stacks.",
        "source": "oa_question",
        "company": "Microsoft",
    },
    {
        "content": "Microsoft OA question: Given a binary tree, serialize it to a string and deserialize it back to the original tree structure.",
        "source": "oa_question",
        "company": "Microsoft",
    },
    {
        "content": "Microsoft interviews commonly cover OOP design principles (SOLID), low-level design questions, and basic familiarity with C#/.NET or equivalent strongly-typed language concepts.",
        "source": "topic_focus",
        "company": "Microsoft",
    },

    # ── Meta ──
    {
        "content": "Meta (Facebook) SWE interviews are known for being fast-paced and coding-heavy, with strong emphasis on writing bug-free code quickly and explaining your approach clearly while coding.",
        "source": "job_description",
        "company": "Meta",
    },
    {
        "content": "Meta interview experience: Two back-to-back 45-minute coding rounds focused on arrays, strings, and graphs, with a strict emphasis on writing fully working code (not just pseudocode) within the time limit.",
        "source": "interview_experience",
        "company": "Meta",
    },
    {
        "content": "Meta interview experience: The behavioral round explicitly probes for 'Move Fast,' 'Be Bold,' and conflict-resolution stories, often asking for a specific example with metrics or measurable outcomes.",
        "source": "interview_experience",
        "company": "Meta",
    },
    {
        "content": "Meta OA question: Given a string, find the length of the longest substring without repeating characters using the sliding window technique.",
        "source": "oa_question",
        "company": "Meta",
    },
    {
        "content": "Meta OA question: Design a news feed ranking system at a high level, discussing data sources, ranking signals, and how you'd evaluate ranking quality.",
        "source": "oa_question",
        "company": "Meta",
    },
    {
        "content": "Meta interviews place unusually high weight on coding speed and correctness under time pressure compared to other big tech companies, with less tolerance for incomplete solutions.",
        "source": "topic_focus",
        "company": "Meta",
    },

    # ── Goldman Sachs ──
    {
        "content": "Goldman Sachs technology analyst interviews mix standard DSA coding rounds with finance-domain awareness, particularly around data integrity, low-latency systems, and risk-aware engineering decisions.",
        "source": "job_description",
        "company": "Goldman Sachs",
    },
    {
        "content": "Goldman Sachs interview experience: HackerRank-style OA first (2-3 DSA problems plus 1 SQL question), followed by 2-3 technical rounds and a final 'superday' with multiple back-to-back interviews in one day.",
        "source": "interview_experience",
        "company": "Goldman Sachs",
    },
    {
        "content": "Goldman Sachs interview experience: Behavioral questions often ask about working under pressure, attention to detail with financial data, and examples of catching or preventing a costly mistake.",
        "source": "interview_experience",
        "company": "Goldman Sachs",
    },
    {
        "content": "Goldman Sachs OA question: Write SQL to find the second-highest salary per department from an employees table, handling ties and nulls correctly.",
        "source": "oa_question",
        "company": "Goldman Sachs",
    },
    {
        "content": "Goldman Sachs OA question: Implement a basic order-matching engine for a simplified stock exchange, matching buy and sell orders by price and time priority.",
        "source": "oa_question",
        "company": "Goldman Sachs",
    },
    {
        "content": "Goldman Sachs technology interviews commonly test SQL proficiency, OOP design, and basic understanding of concurrency and thread safety given their low-latency trading systems.",
        "source": "topic_focus",
        "company": "Goldman Sachs",
    },

    # ── Uber ──
    {
        "content": "Uber SWE interviews focus on practical system design relevant to their domain (ride-matching, real-time location, surge pricing) alongside standard DSA rounds.",
        "source": "job_description",
        "company": "Uber",
    },
    {
        "content": "Uber interview experience: One round commonly asks to design a simplified version of Uber's ride-matching system, discussing how you'd match nearby drivers to riders efficiently at scale.",
        "source": "interview_experience",
        "company": "Uber",
    },
    {
        "content": "Uber interview experience: Behavioral rounds emphasize 'bias for action' and ownership, often asking for an example of identifying and fixing a problem nobody asked you to fix.",
        "source": "interview_experience",
        "company": "Uber",
    },
    {
        "content": "Uber OA question: Given a list of GPS coordinates, find the K nearest drivers to a given rider location efficiently.",
        "source": "oa_question",
        "company": "Uber",
    },
    {
        "content": "Uber OA question: Design a surge pricing algorithm at a high level, discussing what signals you'd use and how you'd avoid abrupt price spikes that frustrate users.",
        "source": "oa_question",
        "company": "Uber",
    },
    {
        "content": "Uber interviews frequently test geospatial data structures (quadtrees, geohashing) and real-time system design given their core ride-matching product.",
        "source": "topic_focus",
        "company": "Uber",
    },

    # ── Salesforce ──
    {
        "content": "Salesforce SWE interviews emphasize OOP design, REST API design, and practical knowledge of building scalable multi-tenant SaaS systems.",
        "source": "job_description",
        "company": "Salesforce",
    },
    {
        "content": "Salesforce interview experience: Rounds typically include 1 DSA round, 1 OOP/low-level design round (e.g. design a parking system using classes), and 1 round on REST API design principles.",
        "source": "interview_experience",
        "company": "Salesforce",
    },
    {
        "content": "Salesforce interview experience: Behavioral questions focus on their core values (Trust, Customer Success, Innovation), often asking for examples of going beyond what was asked to help a user or teammate.",
        "source": "interview_experience",
        "company": "Salesforce",
    },
    {
        "content": "Salesforce OA question: Design a REST API for a simple task management system, including endpoint design, status codes, and pagination strategy.",
        "source": "oa_question",
        "company": "Salesforce",
    },
    {
        "content": "Salesforce OA question: Given a class hierarchy for shapes (Circle, Square, Triangle), implement an area calculator following good OOP principles like polymorphism.",
        "source": "oa_question",
        "company": "Salesforce",
    },
    {
        "content": "Salesforce interviews commonly test multi-tenancy concepts, REST API best practices, and clean OOP design with attention to extensibility.",
        "source": "topic_focus",
        "company": "Salesforce",
    },

    # ── Atlassian ──
    {
        "content": "Atlassian SWE interviews are known for being collaborative and discussion-heavy, valuing clear communication and 'thinking out loud' as much as the final solution's correctness.",
        "source": "job_description",
        "company": "Atlassian",
    },
    {
        "content": "Atlassian interview experience: A signature round is the 'values round,' explicitly discussing their stated company values (like 'Open company, no bullshit') with specific personal examples.",
        "source": "interview_experience",
        "company": "Atlassian",
    },
    {
        "content": "Atlassian interview experience: Coding rounds are collaborative -- the interviewer often actively discusses approach with you mid-problem rather than staying silent, valuing how you respond to hints.",
        "source": "interview_experience",
        "company": "Atlassian",
    },
    {
        "content": "Atlassian OA question: Design a basic Kanban board backend (similar to Jira/Trello), with cards, columns, and the ability to move cards between columns while tracking history.",
        "source": "oa_question",
        "company": "Atlassian",
    },
    {
        "content": "Atlassian OA question: Given a list of user activity logs, implement a function that detects suspicious login patterns based on time and location.",
        "source": "oa_question",
        "company": "Atlassian",
    },
    {
        "content": "Atlassian interviews value collaborative problem-solving and clear verbal communication of your thought process more heavily than pure algorithmic speed compared to Meta or Google.",
        "source": "topic_focus",
        "company": "Atlassian",
    },

    # ── Flipkart ──
    {
        "content": "Flipkart SDE interviews combine strong DSA fundamentals with India-specific e-commerce scale problems -- inventory management, order processing, and high-traffic sale events like Big Billion Days.",
        "source": "job_description",
        "company": "Flipkart",
    },
    {
        "content": "Flipkart interview experience: Rounds include 2 DSA rounds (medium-hard LeetCode style), 1 system design round (often 'design Flipkart's flash sale system'), and a hiring manager round.",
        "source": "interview_experience",
        "company": "Flipkart",
    },
    {
        "content": "Flipkart interview experience: A common system design ask is handling massive traffic spikes during sale events without overselling limited-stock items -- testing understanding of distributed locks and inventory consistency.",
        "source": "interview_experience",
        "company": "Flipkart",
    },
    {
        "content": "Flipkart OA question: Given a stream of orders, design a system to prevent overselling of a product with limited stock under high concurrency.",
        "source": "oa_question",
        "company": "Flipkart",
    },
    {
        "content": "Flipkart OA question: Implement a basic recommendation system that suggests products based on a user's purchase history, discussing the approach at a high level.",
        "source": "oa_question",
        "company": "Flipkart",
    },
    {
        "content": "Flipkart interviews frequently test distributed systems concepts (distributed locks, eventual consistency, idempotency) given their high-concurrency e-commerce domain.",
        "source": "topic_focus",
        "company": "Flipkart",
    },
]

async def seed():
    async with AsyncSessionLocal() as db:
        for item in SEED_DATA:
            print(f"Embedding: {item['content'][:60]}...")
            embedding = generate_embedding(item["content"])  # sync call, no await

            chunk = KnowledgeChunk(
                content=item["content"],
                embedding=embedding,
                source=item["source"],
                company=item["company"],
            )
            db.add(chunk)

        await db.commit()
        print(f"\nSeeded {len(SEED_DATA)} knowledge chunks successfully.")


if __name__ == "__main__":
    asyncio.run(seed())