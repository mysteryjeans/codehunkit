-- Author: Faraz Masood Khan
-- Compute ranks

-- Compute rank based on time of submittion
CREATE OR REPLACE FUNCTION compute_rank(votes integer, post_date timestamp with time zone) RETURNS numeric AS $$
        BEGIN
                RETURN trunc(CAST((log(GREATEST(abs(votes),1)) + (sign(votes) * extract(epoch from post_date)/45000)) AS numeric), 7);
        END;
$$ LANGUAGE plpgsql;


-- Compute rank based on confidence of votes
CREATE OR REPLACE FUNCTION compute_rank(up_votes integer, down_votes integer) RETURNS numeric AS $$
	DECLARE
	    z real := 1.0; -- 1.0 = 85%, 1.6 = 95%	    
	    n integer := up_votes + down_votes;
	    phat real := up_votes / GREATEST(n, 1);
        BEGIN		
		
		IF n = 0 THEN
		   RETURN 0.0;
		END IF;

		RETURN trunc(CAST((sqrt(phat+z*z/(2*n)-z*((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n)) AS numeric), 7);
        END;
$$ LANGUAGE plpgsql;
