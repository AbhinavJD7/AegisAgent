use anchor_lang::prelude::*;

declare_id!("Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS");

#[program]
pub mod aegis_agent {
    use super::*;

    pub fn log_decision(_ctx: Context<LogDecision>, context_hash: String, decision_label: String) -> Result<()> {
        let clock = Clock::get()?;
        emit!(DecisionLogged {
            context_hash,
            decision_label,
            timestamp: clock.unix_timestamp,
        });
        Ok(())
    }
}

#[derive(Accounts)]
pub struct LogDecision {}

#[event]
pub struct DecisionLogged {
    pub context_hash: String,
    pub decision_label: String,
    pub timestamp: i64,
}
