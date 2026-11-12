-- EnsembleStarsAnalyzer 3.3.0-dev / OVERALL PACHINKO leaderboard
-- Run once in Supabase SQL Editor for a NEW project.
create table if not exists public.pachinko_results (
    id uuid primary key default gen_random_uuid(),
    total_notes bigint not null check (total_notes >= 300),
    initial_overall numeric(6,3),
    initial_type text not null check (initial_type in ('NORMAL', 'PITY TIME')),
    initial_spins integer not null check (initial_spins between 1 and 150),
    initial_payout_notes integer not null check (initial_payout_notes in (300, 1500, 3000, 4500, 6000)),
    rush_hits integer not null check (rush_hits >= 0),
    rush_notes bigint not null check (rush_notes >= 0),
    played_at timestamptz not null,
    created_at timestamptz not null default now(),
    constraint pachinko_total_consistency check (total_notes = initial_payout_notes + rush_notes),
    constraint pachinko_initial_type_consistency check (
        (initial_type = 'PITY TIME'
            and initial_overall is null
            and initial_spins = 150
            and initial_payout_notes = 6000)
        or
        (initial_type = 'NORMAL'
            and initial_overall is not null
            and initial_spins between 1 and 150
            and initial_payout_notes in (300, 1500, 3000, 4500))
    )
);

create index if not exists pachinko_results_total_notes_idx
    on public.pachinko_results (total_notes desc, played_at asc, id asc);

alter table public.pachinko_results enable row level security;

drop policy if exists "public can insert pachinko results" on public.pachinko_results;
drop policy if exists "public can read pachinko results" on public.pachinko_results;
drop policy if exists "anon can insert pachinko results" on public.pachinko_results;
drop policy if exists "anon can read pachinko results" on public.pachinko_results;

create policy "anon can insert pachinko results"
    on public.pachinko_results for insert to anon with check (true);
create policy "anon can read pachinko results"
    on public.pachinko_results for select to anon using (true);

grant usage on schema public to anon;
grant select, insert on public.pachinko_results to anon;

-- Competition ranking: tied scores share a rank; the next rank skips.
create or replace function public.get_pachinko_rank_for_score(p_total_notes bigint)
returns table (rank bigint, total_count bigint)
language sql
stable
security invoker
set search_path = public
as $$
    select
        (count(*) filter (where total_notes > p_total_notes) + 1)::bigint as rank,
        count(*)::bigint as total_count
    from public.pachinko_results;
$$;

-- One RPC call returns a page, competition rank, and total row count.
create or replace function public.get_pachinko_leaderboard(
    p_limit integer default 50,
    p_offset integer default 0
)
returns table (
    rank bigint,
    total_count bigint,
    id uuid,
    total_notes bigint,
    initial_overall numeric,
    initial_type text,
    initial_spins integer,
    initial_payout_notes integer,
    rush_hits integer,
    rush_notes bigint,
    played_at timestamptz
)
language sql
stable
security invoker
set search_path = public
as $$
    select
        rank() over (order by r.total_notes desc)::bigint as rank,
        count(*) over ()::bigint as total_count,
        r.id, r.total_notes, r.initial_overall, r.initial_type,
        r.initial_spins, r.initial_payout_notes, r.rush_hits,
        r.rush_notes, r.played_at
    from public.pachinko_results as r
    order by r.total_notes desc, r.played_at asc, r.id asc
    limit greatest(1, least(coalesce(p_limit, 50), 100))
    offset greatest(0, coalesce(p_offset, 0));
$$;

grant execute on function public.get_pachinko_rank_for_score(bigint) to anon;
grant execute on function public.get_pachinko_leaderboard(integer, integer) to anon;
