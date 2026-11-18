/**
 * V4.57: offline-only, deterministic research-pilot scorer.
 * No participants or answers are sent anywhere. This is not wired to the app.
 * The answer key is public in the research repository; moderators must withhold it from participants.
 */
export function scoreReaderSession(instrument, session) {
  if (!instrument || !Array.isArray(instrument.questions) || !Array.isArray(instrument.tasks)) throw Error("invalid instrument");
  if (!session || typeof session !== "object") throw Error("invalid session");
  const choices=session.answers||{};
  const tasks=session.completedTasks||{};
  const valid=new Set(instrument.questions.map(q=>q.id));
  for (const id of Object.keys(choices)) if (!valid.has(id)) throw Error("unknown question: "+id);
  const perQuestion=instrument.questions.map(q=>{
    const choice=choices[q.id]??null;
    if (choice!==null && !q.choices.some(c=>c.id===choice)) throw Error("invalid answer choice: "+q.id);
    return {
      id:q.id,
      correct:choice===q.answerKey,
      unanswered:choice===null,
      critical:q.critical===true,
      misconceptionCode:choice!==null&&choice!==q.answerKey?q.misconceptionCode:null
    };
  });
  const score=perQuestion.filter(q=>q.correct).length;
  const criticalScore=perQuestion.filter(q=>q.critical&&q.correct).length;
  const allTasksCompleted=instrument.tasks.every(t=>tasks[t.id]===true);
  const thresholds=instrument.scoring.individualPass;
  return {
    score, maxScore:instrument.questions.length,
    criticalScore, criticalMax:instrument.scoring.criticalIds.length,
    allTasksCompleted, answered:perQuestion.filter(q=>!q.unanswered).length,
    passed:score>=thresholds.correctAtLeast && criticalScore>=thresholds.criticalCorrectAtLeast && allTasksCompleted,
    perQuestion
  };
}
export function evaluatePilot(instrument, anonymousSessions) {
  if (!Array.isArray(anonymousSessions)) throw Error("sessions must be an array");
  const unique=new Set();
  for (const item of anonymousSessions) {
    if (!/^P[0-9]{2,4}$/.test(item.sessionId||"") || unique.has(item.sessionId)) throw Error("session IDs must be unique anonymous Pnn identifiers");
    unique.add(item.sessionId);
  }
  const totals=anonymousSessions.map(s=>scoreReaderSession(instrument,s));
  const min=instrument.scoring.pilotReviewThreshold.minimumParticipants;
  const passRate=totals.length?totals.filter(s=>s.passed).length/totals.length:0;
  const taskCompletionRate=totals.length
    ?anonymousSessions.reduce((sum,s)=>sum+instrument.tasks.filter(t=>(s.completedTasks||{})[t.id]===true).length,0)/(totals.length*instrument.tasks.length)
    :0;
  const misconceptionCounts={};
  for(const r of totals)for(const q of r.perQuestion)if(q.critical&&q.misconceptionCode)
    misconceptionCounts[q.misconceptionCode]=(misconceptionCounts[q.misconceptionCode]||0)+1;
  const repeatedCritical=Object.entries(misconceptionCounts).filter(([,n])=>n>=instrument.scoring.pilotReviewThreshold.repeatCriticalMisconceptionThreshold);
  const reviewEligible=totals.length>=min && passRate>=instrument.scoring.pilotReviewThreshold.individualPassRateAtLeast
    && taskCompletionRate>=instrument.scoring.pilotReviewThreshold.taskCompletionRateAtLeast
    && repeatedCritical.length===0;
  return {
    actualParticipants:totals.length,
    minimumParticipantsMet:totals.length>=min,
    passRate,taskCompletionRate,repeatedCritical,
    reviewEligible,
    historicExpertApproved:false,
    canShip:false
  };
}
